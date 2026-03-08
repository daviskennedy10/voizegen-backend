from app.database import SessionLocal
from app.models.curriculum import Section, Unit, Lesson
from app.models.exercise import PhonemeExercise

# Open a database session — this is our "conversation" with the DB
db = SessionLocal()

# ── STEP 1: Create a Section ──────────────────────────────────────────
# This is the top-level grouping in the curriculum
section = Section(
    title="Phoneme Practice",
    order_index=1
)
db.add(section)       # Stage it (like git add)
db.flush()            # Send to DB so section.id gets generated, but don't commit yet

# ── STEP 2: Create a Unit inside that Section ─────────────────────────
unit = Unit(
    title="Basic Sounds",
    order_index=1,
    section_id=section.id,   # Link to the section we just created
    unlock_condition=None     # First unit is always unlocked
)
db.add(unit)
db.flush()

# ── STEP 3: Create a Lesson inside that Unit ──────────────────────────
lesson = Lesson(
    title="Starter Phonemes",
    order_index=1,
    type="phoneme",           # Tells the frontend which exercise component to render
    unit_id=unit.id           # Link to the unit we just created
)
db.add(lesson)
db.flush()

# ── STEP 4: Create 5 Phoneme Exercises inside that Lesson ─────────────
# These are the actual exercises a child will practice
exercises = [
    PhonemeExercise(
        lesson_id=lesson.id,
        phoneme="sh",
        instruction_text="Say the sound: SH (like in 'shoe')",
        audio_url=None,   # We'll add real audio URLs later
        matched=None      # None means not attempted yet
    ),
    PhonemeExercise(
        lesson_id=lesson.id,
        phoneme="ch",
        instruction_text="Say the sound: CH (like in 'chair')",
        audio_url=None,
        matched=None
    ),
    PhonemeExercise(
        lesson_id=lesson.id,
        phoneme="th",
        instruction_text="Say the sound: TH (like in 'think')",
        audio_url=None,
        matched=None
    ),
    PhonemeExercise(
        lesson_id=lesson.id,
        phoneme="ee",
        instruction_text="Say the sound: EE (like in 'feet')",
        audio_url=None,
        matched=None
    ),
    PhonemeExercise(
        lesson_id=lesson.id,
        phoneme="oo",
        instruction_text="Say the sound: OO (like in 'moon')",
        audio_url=None,
        matched=None
    ),
]

# Add all 5 exercises at once
db.add_all(exercises)

# ── STEP 5: Commit everything ─────────────────────────────────────────
# This is like git commit — nothing is permanently saved until this runs.
# If anything above failed, nothing gets saved (all or nothing).
db.commit()

print("✅ Seed complete!")
print(f"   Section: {section.title} (id: {section.id})")
print(f"   Unit: {unit.title} (id: {unit.id})")
print(f"   Lesson: {lesson.title} (id: {lesson.id})")
print(f"   Exercises: {len(exercises)} phoneme exercises created")

db.close()