from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

# A Section is the top level of the curriculum.
# Example: "Social Interactions", "Phoneme Practice"
class Section(Base):
    __tablename__ = "sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)

    # order_index controls which section appears first, second, etc.
    # So section with order_index=1 always shows before order_index=2.
    order_index = Column(Integer, nullable=False)

    # relationship() tells SQLAlchemy that one Section has many Units.
    # back_populates means a Unit can also access its parent Section via unit.section
    units = relationship("Unit", back_populates="section")


# A Unit lives inside a Section.
# Example: Section="Phoneme Practice" → Unit="Basic Sounds"
class Unit(Base):
    __tablename__ = "units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)

    # ForeignKey links this unit to its parent section.
    # If you delete a section, you'd need to handle its units too.
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)

    # unlock_condition lets you say "only unlock this unit after completing another"
    # nullable=True means it can be empty (first unit is always unlocked)
    unlock_condition = Column(String, nullable=True)

    section = relationship("Section", back_populates="units")
    lessons = relationship("Lesson", back_populates="unit")


# A Lesson lives inside a Unit.
# type tells us what kind of lesson it is: "phoneme", "word", or "story"
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)

    # "phoneme" | "word" | "story" — determines which exercises to load
    type = Column(String, nullable=False)

    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)

    unit = relationship("Unit", back_populates="lessons")
    phoneme_exercises = relationship("PhonemeExercise", back_populates="lesson")