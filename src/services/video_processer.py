import json
import os
from datetime import datetime, timedelta
from typing import Any

import cv2
import numpy as np
import structlog
from scipy import stats as st
from ultralytics import YOLO

from database.crud import add_result_detect, get_start_data
from helpers.helpers import Helpers

from .config import Config

logger = structlog.get_logger()


class VideoProcesser:
    """
    Service for processing recorded videos to obtain data on detected products.
    """

    def __init__(self) -> None:
        self.config = Config()
        self.helpers = Helpers()

    def send_data(
        self, tray_id: int, bread_amount: list[int], detected_time: datetime
    ) -> None:
        """
        Insert tray data to the database.

        :param tray_id: id of the tray
        :param bread_amount: the amount of bread in the tray
        :param detected_time: time of detected tray
        """
        with open("start_data.json", "r") as f:
            data = json.load(f)

        for i, count_of_loaf in enumerate(bread_amount[1:11]):
            if count_of_loaf > 0:
                sku_id = i + 1

                if sku_id != data["last_change_sku"]:
                    data["last_change_sku"] = sku_id
                    data["last_change_sku_time"] = detected_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    with open("start_data.json", "w") as f:
                        json.dump(data, f)

                content = {
                    "tray_id": tray_id,
                    "sku_id": sku_id,
                    "count_of_loaf": count_of_loaf,
                    "deviation_detected": count_of_loaf != 8,
                    "last_change_sku_time": data["last_change_sku_time"],
                    "detected_time": detected_time,
                }
                add_result_detect(content)

    def process_inter_data(
        self,
        is_covered: int,
        bread_amount: list[list[int]],
        tray_id: int,
        start_roi: np.ndarray[Any],
        finish_roi: np.ndarray[Any],
        model: YOLO,
        detected_time: datetime,
        roi: np.ndarray[Any],
    ) -> tuple[int, list, int]:
        """
        Process video frame and get model predictions.

        :param is_covered: the amount of subsequent frames in which the tray was present
        :param bread_amount: the amount of predicted SKU
        :param tray_id: id of the current tray
        :param start_roi: first roi to understand if the tray is in the main roi
        :param finish_roi: second roi to understand if the tray is in the main roi
        :param model: the YOLO model
        :param detected_time: time the tray appeared
        :param roi: the main roi
        :return is_covered: the amount of subsequent frames in which the tray was present
        :return bread_amount: the amount of predicted SKU
        :return tray_id: id of the current tray
        """
        if (
            np.count_nonzero(start_roi == 0) / (start_roi.shape[0] * start_roi.shape[1])
            >= 0.6
            and np.count_nonzero(finish_roi == 0)
            / (finish_roi.shape[0] * finish_roi.shape[1])
            >= 0.6
        ):
            is_covered += 1
        else:
            if is_covered < 11 and bread_amount != [
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ]:
                bread_amount = [
                    int(st.mode(i).mode) if len(i) > 2 else 0 for i in bread_amount
                ]

                if bread_amount[0] > 0 and sum(bread_amount[1:11]) < 12:
                    self.send_data(
                        tray_id=tray_id,
                        bread_amount=bread_amount,
                        detected_time=detected_time,
                    )
                    tray_id += 1
            is_covered = 0
            bread_amount = [[], [], [], [], [], [], [], [], [], [], [], []]

        # predict if basket in roi less than 11 frames
        if 0 < is_covered < 11:
            # predict bboxes
            results = (
                model.predict(roi, conf=0.6, verbose=False)[0]
                .boxes.data.numpy()
                .astype(int)
            )

            # get number of breads
            unq, counts = np.unique(results[:, -1], return_counts=True)

            for i in range(len(unq)):
                bread_amount[unq[i]].append(counts[i])

        # if 10 frames were sequentially covered then count most frequent value of bread counted
        elif is_covered == 11:
            bread_amount = [
                int(st.mode(i).mode) if len(i) > 2 else 0 for i in bread_amount
            ]

            # if basket was detected, then send data to db
            if bread_amount[0] > 0 and sum(bread_amount[1:11]) < 12:
                self.send_data(
                    tray_id=tray_id,
                    bread_amount=bread_amount,
                    detected_time=detected_time,
                )
                tray_id += 1

        return is_covered, bread_amount, tray_id

    def cut_grayscale_roi(
        self, x1: int, y1: int, x2: int, y2: int, roi: np.ndarray[Any]
    ) -> np.ndarray[Any]:
        """
        Cut roi to specified dimentions and get image filtered
        :param x1: left-top x-coordinate
        :param y1: left-top y-coordinate
        :param x2: right-bottom x-coordinate
        :param y2: right-bottom y-coordinate
        :param roi: main roi
        :return roi: filtered and cut roi
        """
        roi = roi[y1:y2, x1:x2, :].copy()
        roi[(roi[:, :, 0] > roi[:, :, 1]) & (roi[:, :, 0] > roi[:, :, 2])] = (
            255,
            255,
            255,
        )
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi[roi != 255] = 0

        return roi.copy()

    def process_video(
        self,
        model: any,
        cap: any,
        ms_per_frame: float,
        detected_time: datetime,
        is_covered: any,
        bread_amount: any,
        tray_id: int,
    ) -> int:
        """
        Process video.

        :param model:
        :param cap:
        :param ms_per_frame:
        :param detected_time:
        :param is_covered:
        :param bread_amount:
        :param tray_id:
        """
        count_frames = 0

        while True:
            ret, frame = cap.read()
            count_frames += 1

            if not ret:
                break

            # resize frame for better processing
            frame = cv2.resize(frame, (1280, 720))

            # cut roi
            dy, dx, _ = frame.shape
            x1, x2, y1, y2 = (
                int(350 / 1280 * dx),
                int(1050 / 1280 * dx),
                int(190 / 720 * dy),
                int(580 / 720 * dy),
            )
            roi = frame[y1:y2, x1:x2, :]

            # shape settings for new roi
            dy, dx, _ = roi.shape
            dx //= 5
            dy //= 5

            # define start and finish of the roi
            start = self.cut_grayscale_roi(-2 * dx, dy, -dx, -dy, roi)
            finish = self.cut_grayscale_roi(dx, dy, 2 * dx, -dy, roi)

            # process intermediate data
            is_covered, bread_amount, tray_id = self.process_inter_data(
                is_covered,
                bread_amount,
                tray_id,
                start,
                finish,
                model,
                detected_time,
                roi,
            )

            if count_frames == ms_per_frame:
                count_frames = 0
                detected_time += timedelta(seconds=1)

        return tray_id

    def run(self, model, tray_id: int) -> None:
        """
        Get videofile name and remove processed videos.

        :param model:
        :param tray_id:
        """
        is_covered = 0
        bread_amount = [[], [], [], [], [], [], [], [], [], [], [], []]

        logger.info("Получаем видео")
        while True:
            video = list(
                filter(
                    lambda x: x.endswith((".mkv", ".mp4")),
                    sorted(os.listdir(self.config.video_path)),
                )
            )
            if video:
                video = video[0]
            else:
                continue

            detected_time = datetime.strptime(video, f"%Y-%m-%dT%H-%M-%S.{video[-3:]}")
            if (
                datetime.now() - timedelta(seconds=self.config.video_length_s)
                <= detected_time
            ):
                continue

            logger.info(f"Starting processing {video} video")
            cap = cv2.VideoCapture(f"{self.config.video_path}/{video}")

            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps > 60:
                fps = 24
            ms_per_frame = fps

            tray_id = self.process_video(
                model,
                cap,
                ms_per_frame,
                detected_time,
                is_covered,
                bread_amount,
                tray_id,
            )
            tray_id += 1

            logger.info(f"Обработали и удалили {video}")
            os.remove(f"{self.config.video_path}/{video}")
            logger.info(f"File {self.config.video_path}/{video} has been removed")

    def start_model(self):
        """
        Initialize model and start video processing.
        """
        logger.info("Инициализируем модель")
        model = YOLO(self.config.model_path / self.config.model_name)

        logger.info("Добавляем дефолтные данные если их нет ")
        self.helpers.add_default_product()

        logger.info("Получаем первичные данные для работы")
        tray_id, last_change_sku, last_change_sku_time = get_start_data()

        content = {
            "last_change_sku": last_change_sku,
            "last_change_sku_time": last_change_sku_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open("start_data.json", "w") as f:
            json.dump(content, f)

        self.run(model, tray_id)
