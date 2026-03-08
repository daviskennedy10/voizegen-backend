from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

# This import ensures Lesson is registered with SQLAlchemy
# before PhonemeExercise tries to reference it
from app.models.curriculum import Lesson

# A PhonemeExercise is one individual exercise inside a Lesson.
# The child hears a phoneme, speaks it, and we check if they matched it.
class PhonemeExercise(Base):
    __tablename__ = "phoneme_exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Which lesson this exercise belongs to
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)

    # The actual phoneme sound, e.g. "sh", "ch", "th"
    phoneme = Column(String, nullable=False)

    # What the UI shows the child: "Say the sound: SH"
    instruction_text = Column(String, nullable=False)

    # URL to the audio file of the correct pronunciation (stored in Firebase Storage later)
    audio_url = Column(String, nullable=True)

    # matched gets set to True or False after the child speaks
    # We store this per-attempt so parents can see history
    matched = Column(Boolean, nullable=True)

    lesson = relationship("Lesson", back_populates="phoneme_exercises")