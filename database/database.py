from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import SettingsPostgres

username = SettingsPostgres.DB_USERNAME
password = SettingsPostgres.DB_PASSWORD
host = SettingsPostgres.DB_HOST
port = SettingsPostgres.DB_PORT
db = SettingsPostgres.DB_NAME

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{db}")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
