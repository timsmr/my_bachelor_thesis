from pydantic import Field
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    """Database configuration."""

    db_name: str = Field("postgres", env="DB_NAME")
    db_password: str = Field("admin", env="DB_PASSWORD")
    db_username: str = Field("postgres", env="DB_USERNAME")
    db_port: int = Field(5432, env="DB_PORT")
    db_host: str = Field("postgres", env="DB_HOST")

    class Config:
        env_file = "./.env"
        extra = "allow"
