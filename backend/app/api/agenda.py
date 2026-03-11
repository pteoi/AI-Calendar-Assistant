from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import datetime
from app.models.domain import EventDB
from app.models.schemas import EventCreate, EventResponse
from app.database import get_db

router = APIRouter(tags=["Agenda"])


@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    scheduled_events = db.query(EventDB).all()
    for e in scheduled_events:
        if event.datetime <= e.datetime < event.datetime + datetime.timedelta(
            minutes=event.duration
        ) or e.datetime <= event.datetime < e.datetime + datetime.timedelta(
            minutes=e.duration
        ):
            raise HTTPException(
                status_code=400, detail=f"{e.name} is already scheduled for this time."
            )

    new_event = EventDB(
        name=event.name,
        datetime=event.datetime,
        duration=event.duration,
        description=event.description,
        repeats=event.repeats,
        repeat_interval=event.repeat_interval,
        repeats_until=event.repeats_until,

    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get("/", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(EventDB).all()
    return events


@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"detail": "Event deleted successfully"}
