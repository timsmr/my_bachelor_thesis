from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DBConfig

config = DBConfig()

engine = create_engine(
    f"postgresql://{config.db_username}:\
{config.db_password}@{config.db_host}:\
{config.db_port}/{config.db_name}"
)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
