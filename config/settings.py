import os

from dotenv import load_dotenv

load_dotenv()


class SettingModel:
    MODEL_PATH = "best.pt"
    VIDEO_PATH = "videos"
    RTSP_URL = os.getenv('RTSP_URL', "rtsp://localhost:8554/live.stream")


class SettingsPostgres:
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
    DB_NAME = os.getenv("DB_NAME", "postgres")
