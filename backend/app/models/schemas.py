from pydantic import BaseModel, Field
from datetime import datetime as dt
from typing import Optional


class EventBase(BaseModel):
    name: str = Field(..., description="The name of the event")
    datetime: dt = Field(
        ..., description="The date and time of the event (YYYY-MM-DD HH:MM format)"
    )
    duration: int = Field(..., description="The duration of the event in minutes")
    description: Optional[str] = Field(None, description="A description of the event")
    repeats: Optional[bool] = Field(False, description="Whether the event repeats")
    repeat_interval: Optional[int] = Field(
        0, description="The interval in days for repeating events"
    )
    repeats_until: Optional[dt] = Field(
        None, description="The date until which the event repeats (YYYY-MM-DD format)"
    )


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int

    class Config:
        from_attributes = True
