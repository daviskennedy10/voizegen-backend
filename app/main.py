from fastapi import FastAPI
from app.database import engine, Base

# Model imports — needed so SQLAlchemy knows about all tables
from app.models import user
from app.models import curriculum
from app.models import exercise

# Route imports — these were missing before
from app.routes import curriculum as curriculum_routes
from app.routes import exercises as exercise_routes
from app.routes import speech as speech_routes

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(title="Voizegen API", version="1.0.0")

# Register all routers
app.include_router(curriculum_routes.router)
app.include_router(exercise_routes.router)
app.include_router(speech_routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Voizegen backend is running"}