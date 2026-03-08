from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.curriculum import Section, Unit, Lesson

# APIRouter is like a mini FastAPI app for just this feature.
# We'll register it in main.py. This keeps routes organized —
# curriculum routes live here, speech routes live in speech.py, etc.
router = APIRouter(prefix="/curriculum", tags=["Curriculum"])

@router.get("")
def get_curriculum(db: Session = Depends(get_db)):
    # Depends(get_db) is FastAPI's dependency injection.
    # It automatically opens a DB session, passes it here, and closes
    # it when the request is done. You never call get_db() yourself.

    # joinedload tells SQLAlchemy to fetch related records in the same
    # query instead of making separate DB calls for each unit/lesson.
    # Without this, fetching 10 sections would make 10+ extra queries.
    sections = (
        db.query(Section)
        .options(
            joinedload(Section.units).joinedload(Unit.lessons)
        )
        .order_by(Section.order_index)
        .all()
    )

    # We manually build the response shape here so we control exactly
    # what the frontend receives. Never expose raw DB objects directly.
    result = []
    for section in sections:
        result.append({
            "id": str(section.id),
            "title": section.title,
            "order_index": section.order_index,
            "units": [
                {
                    "id": str(unit.id),
                    "title": unit.title,
                    "order_index": unit.order_index,
                    "unlock_condition": unit.unlock_condition,
                    "lessons": [
                        {
                            "id": str(lesson.id),
                            "title": lesson.title,
                            "type": lesson.type,
                            "order_index": lesson.order_index,
                        }
                        for lesson in sorted(unit.lessons, key=lambda l: l.order_index)
                    ]
                }
                for unit in sorted(section.units, key=lambda u: u.order_index)
            ]
        })

    return result