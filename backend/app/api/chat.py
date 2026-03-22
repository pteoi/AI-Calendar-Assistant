from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.domain import EventDB, TaskDB
from app.services.ollama import analyze_event_from_text

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    
    try:
        data = analyze_event_from_text(request.message)

        if data["type"] == "event":
            try:
                data_datetime = datetime.strptime(data["datetime"], "%Y-%m-%dT%H:%M")
            except ValueError:
                data_datetime = datetime.fromisoformat(data["datetime"])

            new_event = EventDB(
                name=data["name"],
                datetime=data_datetime,
                location=data.get("location"),
                duration=data.get("duration"),
                description=data.get("description", ""),
                repeats=data.get("repeats", False),
                repeat_interval=data.get("repeat_interval", 0),
                repeats_until=(
                    datetime.fromisoformat(data["repeats_until"])
                    if data.get("repeats_until")
                    else None
                ),
            )

            db.add(new_event)
            db.commit()
            db.refresh(new_event)

            return {
                "reply": f"Event '{new_event.name}' scheduled for {new_event.datetime.strftime('%b %d, %Y at %H:%M')}.",
                "event": {
                    "id": new_event.id,
                    "name": new_event.name,
                    "datetime": new_event.datetime.isoformat(),
                    "duration": new_event.duration,
                    "description": new_event.description,
                    "repeats": new_event.repeats,
                    "repeat_interval": new_event.repeat_interval,
                    "repeats_until": (
                        new_event.repeats_until.isoformat()
                        if new_event.repeats_until
                        else None
                    ),
                },
            }
        elif data["type"] == "task":
            try:
                data_deadline = datetime.strptime(data["deadline"], "%Y-%m-%dT%H:%M")
            except ValueError:
                data_deadline = datetime.fromisoformat(data["deadline"])

            new_task = TaskDB(
                name=data["name"],
                deadline=data_deadline,
                description=data.get("description", ""),
            )

            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            return {
                "reply": f"Task '{new_task.name}' scheduled with deadline {new_task.deadline.strftime('%b %d, %Y at %H:%M')}.",
                "task": {
                    "id": new_task.id,
                    "name": new_task.name,
                    "deadline": new_task.deadline.isoformat(),
                    "description": new_task.description,
                },
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
