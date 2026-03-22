from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import datetime
from app.models.domain import EventDB, TaskDB
from app.models.schemas import EventCreate, EventResponse, TaskCreate, TaskResponse 
from app.database import get_db

router = APIRouter(tags=["Agenda"])


@router.post("/events", response_model=EventResponse)
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
        location=event.location,
        description=event.description,
        repeats=event.repeats,
        repeat_interval=event.repeat_interval,
        repeats_until=event.repeats_until,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskDB(
        name=task.name,
        deadline=task.deadline,
        description=task.description,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/events", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(EventDB).all()
    return events

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return tasks

@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"detail": "Event deleted successfully"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
