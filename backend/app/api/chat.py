from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.domain import EventDB
from app.services.ollama import analyze_event_from_text

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        event_data = analyze_event_from_text(request.message)
        try: 
            event_datetime = datetime.strptime(event_data["datetime"], "%Y-%m-%dT%H:%M")
        except ValueError:
            event_datetime = datetime.fromisoformat(event_data["datetime"])

        new_event = EventDB(
            name=event_data["name"],
            datetime=event_datetime,
            duration=event_data.get("duration"),
            description=event_data.get("description", ""),
            repeats=event_data.get("repeats", False),
            repeat_interval=event_data.get("repeat_interval", 0),
            repeats_until=datetime.fromisoformat(event_data["repeats_until"]) if event_data.get("repeats_until") else None
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
                "repeats_until": new_event.repeats_until.isoformat() if new_event.repeats_until else None
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))