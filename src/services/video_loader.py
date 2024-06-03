import subprocess

import cv2
import structlog

from .config import Config

logger = structlog.get_logger()


class VideoLoader:
    """
    Service for uploading videos via RTSP protocol with camera availability check.
    """

    def __init__(self) -> None:
        self.config = Config()

    def check_camera_availability(self) -> bool:
        """
        Check if camera is available.
        """
        try:
            cap = cv2.VideoCapture(self.config.rtsp_url)
            if cap.isOpened():
                cap.release()
                return True
        except Exception as e:
            logger.error(f"Ошибка при проверке доступности камеры: {e}")

        return False

    def download_video(self) -> None:
        """
        Download video using ffmpeg tool and subprocess library.
        """
        command = f"ffmpeg -hide_banner -y -loglevel error -rtsp_transport \
            tcp -use_wallclock_as_timestamps 1 -i {self.config.rtsp_url} \
            -vcodec copy -acodec copy -t 300 -f segment -r 24 \
            -segment_format mkv -segment_time {self.config.video_length_s} \
            -strftime 1 {self.config.video_path}/%Y-%m-%dT%H-%M-%S.mkv < /dev/null"

        try:
            subprocess.check_output(command, shell=True)
            logger.info("Видео успешно загружено!")
        except subprocess.CalledProcessError:
            logger.error("Ошибка при загрузке видео.")

    def start_load_video(self) -> None:
        """
        Start video loading process
        """
        while True:
            if self.check_camera_availability():
                logger.info("Камера доступна.")
                self.download_video()
            else:
                logger.error("Камера недоступна.")
