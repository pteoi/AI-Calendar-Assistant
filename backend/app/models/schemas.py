from pydantic import BaseModel, Field
from datetime import datetime as dt
from typing import Optional


class EventBase(BaseModel):
    name: str = Field(..., description="The name of the event")
    datetime: dt = Field(
        ..., description="The date and time of the event (YYYY-MM-DD HH:MM format)"
    )
    duration: int = Field(..., description="The duration of the event in minutes")
    location: Optional[str] = Field(None, description="The location of the event")
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

class TaskBase(BaseModel):
    name: str = Field(..., description="The name of the task")
    deadline: dt = Field(
        ..., description="The deadline of the task (YYYY-MM-DD HH:MM format)"
    )
    description: Optional[str] = Field(None, description="A description of the task")

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True