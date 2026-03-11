from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from app.database import Base


class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    duration = Column(Integer, default=60)
    # location (to be implemented)
    description = Column(String, default="No description provided")
    repeats = Column(Boolean, default=False)
    repeat_interval = Column(Integer, default=0)
    repeats_until = Column(DateTime, default=None, nullable=True)
