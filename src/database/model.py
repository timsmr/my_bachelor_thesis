import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from database.database import Base, engine


class Result(Base):
    __tablename__ = "result"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tray_id = Column(Integer)
    sku_id = Column(Integer)
    count_of_loaf = Column(Integer)
    deviation_detected = Column(Boolean)
    detected_time = Column(DateTime, default=datetime.now())
    last_change_sku_time = Column(DateTime)
    process_by_1c = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sku = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())


Base.metadata.create_all(engine)
