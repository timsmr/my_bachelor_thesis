from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration."""

    local_path: Path = Path(__file__).resolve().parent.parent.parent

    model_name: str = Field(..., env="MODEL_NAME")
    model_path: Path = local_path / "models"

    video_path: Path = local_path / "videos"
    video_length_s: int = Field(300, env="VIDEO_LENGTH_S")

    rtsp_url: str = Field(..., env="RTSP_URL")
