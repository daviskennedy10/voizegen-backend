from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exercise import PhonemeExercise
import uuid

router = APIRouter(prefix="/lessons", tags=["Exercises"])

@router.get("/{lesson_id}/exercises")
def get_exercises(lesson_id: str, db: Session = Depends(get_db)):
    # {lesson_id} in the path becomes a parameter here automatically.
    # FastAPI reads it from the URL and passes it into the function.

    # Validate it's actually a UUID before hitting the DB.
    # If someone sends /lessons/banana/exercises we return a clean error.
    try:
        lesson_uuid = uuid.UUID(lesson_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid lesson ID format")

    # HTTPException is FastAPI's way of returning error responses.
    # status_code=404 means "not found" — the frontend knows to handle this.

    exercises = (
        db.query(PhonemeExercise)
        .filter(PhonemeExercise.lesson_id == lesson_uuid)
        .all()
    )

    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found for this lesson")

    return [
        {
            "id": str(ex.id),
            "phoneme": ex.phoneme,
            "instruction_text": ex.instruction_text,
            "audio_url": ex.audio_url,
            "matched": ex.matched,
        }
        for ex in exercises
    ]
