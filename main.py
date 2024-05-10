import os
import subprocess
from datetime import datetime, timedelta
from typing import Any
import threading

import cv2
import json
import numpy as np
from loguru import logger
from scipy import stats as st
from ultralytics import YOLO

from config.settings import SettingModel
from database import crud
from helpers import helpers


def send_data(tray_id: int, bread_amount: int, detected_time: datetime) -> None:
    """Inserts tray data to the database.

    Args:
    ----
        tray_id (int) -- id of the tray
        bread_amount (int) -- the amount of bread in the tray
        detected_time (datetime) -- time of detected tray
    """
    with open("start_data.json", "r") as f:
        data = json.load(f)

    for i, count_of_loaf in enumerate(bread_amount[1: 11]):
        if count_of_loaf > 0:
            sku_id = i + 1

            if sku_id != data['last_change_sku']:
                data['last_change_sku'] = sku_id
                data['last_change_sku_time'] = detected_time.strftime(
                    "%Y-%m-%d %H:%M:%S")

                with open("start_data.json", "w") as f:
                    json.dump(data, f)

            content = {
                "tray_id": tray_id,
                "sku_id": sku_id,
                "count_of_loaf": count_of_loaf,
                "deviation_detected": count_of_loaf != 8,
                "last_change_sku_time": data['last_change_sku_time'],
                "detected_time": detected_time,
            }
            crud.add_result_detect(content)


def cut_grayscale_roi(x1: int, y1: int, x2: int, y2: int, roi: np.ndarray[Any]) -> np.ndarray[Any]:
    new = roi[y1:y2, x1:x2, :].copy()
    new[(new[:, :, 0] > new[:, :, 1]) & (
        new[:, :, 0] > new[:, :, 2])] = (255, 255, 255)
    new = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    new[new != 255] = 0

    return new.copy()


def process_inter_data(is_covered: int, bread_amount: list[list[int]], tray_id: int, start_roi: np.ndarray[Any],
                       finish_roi: np.ndarray[Any], model: YOLO, detected_time: datetime, roi: any) -> tuple[
        int, list[int], int]:
    if np.count_nonzero(start_roi == 0) / (start_roi.shape[0] * start_roi.shape[1]) >= 0.6 and np.count_nonzero(
            finish_roi == 0) / (finish_roi.shape[0] * finish_roi.shape[1]) >= 0.6:
        is_covered += 1
    else:
        if is_covered < 11 and bread_amount != [[], [], [], [], [], [], [], [], [], [], [], []]:
            bread_amount = [int(st.mode(i).mode) if len(
                i) > 2 else 0 for i in bread_amount]

            if bread_amount[0] > 0 and sum(bread_amount[1: 11]) < 12:
                send_data(tray_id=tray_id, bread_amount=bread_amount,
                          detected_time=detected_time)
                tray_id += 1
        is_covered = 0
        bread_amount = [[], [], [], [], [], [], [], [], [], [], [], []]

    # predict if basket in roi less than 11 frames
    if 0 < is_covered < 11:
        # predict bboxes
        results = model.predict(roi, conf=0.6, verbose=False)[
            0].boxes.data.numpy().astype(int)

        # get number of breads
        unq, counts = np.unique(results[:, -1], return_counts=True)

        for i in range(len(unq)):
            bread_amount[unq[i]].append(counts[i])

    # if 10 frames were sequentially covered then count most frequent value of bread counted
    elif is_covered == 11:
        bread_amount = [int(st.mode(i).mode) if len(i) >
                        2 else 0 for i in bread_amount]

        # if basket was detected, then send data to db
        if bread_amount[0] > 0 and sum(bread_amount[1: 11]) < 12:
            send_data(tray_id=tray_id, bread_amount=bread_amount,
                      detected_time=detected_time)
            tray_id += 1

    return is_covered, bread_amount, tray_id


def process_video(model: any, cap: any, ms_per_frame: float, detected_time: datetime, is_covered: any,
                  bread_amount: any,
                  tray_id: int) -> int:
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
        x1, x2, y1, y2 = int(350 / 1280 * dx), int(1050 /
                                                   1280 * dx), int(190 / 720 * dy), int(580 / 720 * dy)
        roi = frame[y1:y2, x1:x2, :]

        # shape settings for new roi
        dy, dx, _ = roi.shape
        dx //= 5
        dy //= 5

        # define start and finish of the roi
        start = cut_grayscale_roi(-2 * dx, dy, -dx, -dy, roi)
        finish = cut_grayscale_roi(dx, dy, 2 * dx, -dy, roi)

        # process intermediate data
        is_covered, bread_amount, tray_id = process_inter_data(is_covered, bread_amount, tray_id, start, finish,
                                                               model, detected_time, roi)
        logger.info(f"{count_frames} has been processed")
        if count_frames == ms_per_frame:
            count_frames = 0
            detected_time += timedelta(seconds=1)

    return tray_id


def run(model, tray_id: int) -> None:
    is_covered = 0
    bread_amount = [[], [], [], [], [], [], [], [], [], [], [], []]

    logger.info("Получаем видео")
    while True:
        video = list(filter(lambda x: x.endswith((".mkv", ".mp4")),
                     sorted(os.listdir(SettingModel.VIDEO_PATH))))
        if video:
            video = video[0]
        else:
            continue

        detected_time = datetime.strptime(
            video, f"%Y-%m-%dT%H-%M-%S.{video[-3:]}")
        if datetime.now() - timedelta(minutes=5) <= detected_time:
            continue

        cap = cv2.VideoCapture(f"{SettingModel.VIDEO_PATH}/{video}")
        fps = cap.get(cv2.CAP_PROP_FPS)
        ms_per_frame = fps

        logger.info(f'FPS: {fps}')

        tray_id = process_video(model, cap, ms_per_frame,
                                detected_time, is_covered, bread_amount, tray_id)
        tray_id += 1

        logger.success(f"Обработали и удалили {video}")
        os.remove(f"{SettingModel.VIDEO_PATH}/{video}")
        logger.info(f"File {SettingModel.VIDEO_PATH}/{video} has been removed")


def start_model():
    logger.info("Инициализируем модель")
    model = YOLO(SettingModel.MODEL_PATH)

    logger.info("Добавляем дефолтные данные если их нет ")
    helpers.add_default_product()

    logger.info("Получаем первичные данные для работы")
    tray_id, last_change_sku, last_change_sku_time = crud.get_start_data()

    content = {"last_change_sku": last_change_sku,
               "last_change_sku_time": last_change_sku_time.strftime("%Y-%m-%d %H:%M:%S")}
    with open("start_data.json", "w") as f:
        json.dump(content, f)

    run(model, tray_id)


def check_camera_availability():
    rtsp_url = SettingModel.RTSP_URL
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            cap.release()
            return True
    except Exception as e:
        logger.error(f"Ошибка при проверке доступности камеры: {e}")

    return False


def download_video():
    command = f'ffmpeg -hide_banner -y -loglevel error -rtsp_transport tcp -use_wallclock_as_timestamps 1 -i {SettingModel.RTSP_URL} -vcodec copy -acodec copy -t 300 -f segment -segment_format mkv -segment_time 300 -strftime 1 {SettingModel.VIDEO_PATH}/%Y-%m-%dT%H-%M-%S.mkv < /dev/null'

    try:
        subprocess.check_output(command, shell=True)
        logger.success("Видео успешно загружено!")
    except subprocess.CalledProcessError:
        logger.error("Ошибка при загрузке видео.")


def start_load_video():
    while True:
        if check_camera_availability():
            logger.success("Камера доступна.")
            download_video()
        else:
            logger.error("Камера недоступна.")


if __name__ == "__main__":
    thread1 = threading.Thread(target=start_load_video)
    thread2 = threading.Thread(target=start_model)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
