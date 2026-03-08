from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exercise import PhonemeExercise
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

router = APIRouter(prefix="/speech", tags=["Speech"])

# Initialize the OpenAI client once when this file loads.
# It automatically reads OPENAI_API_KEY from your environment.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/check")
async def check_speech(
    exercise_id: str = Form(...),
    audio: UploadFile = File(...),
    mock: bool = Form(False),   # Add this line
    db: Session = Depends(get_db)
):
    try:
        ex_uuid = uuid.UUID(exercise_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid exercise ID")

    exercise = db.query(PhonemeExercise).filter(PhonemeExercise.id == ex_uuid).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # If mock=True, skip Whisper entirely and simulate a match
    if mock:
        heard_text = exercise.phoneme  # Pretend we heard exactly the right sound
        matched = True
    else:
        audio_bytes = await audio.read()
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=(audio.filename or "audio.webm", audio_bytes, audio.content_type),
                language="en"
            )
            heard_text = transcript.text.strip().lower()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Whisper error: {str(e)}")
        matched = exercise.phoneme.lower() in heard_text

    exercise.matched = matched
    db.commit()

    return {
        "exercise_id": exercise_id,
        "heard": heard_text,
        "target": exercise.phoneme,
        "matched": matched,
        "mode": "mock" if mock else "whisper"
    }