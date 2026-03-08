from fastapi import FastAPI
from app.database import engine, Base

# This creates all the tables in your database based on your models.
# It reads every class that inherits from Base and creates the table if
# it doesn't already exist. Safe to run multiple times.
Base.metadata.create_all(bind=engine)

# This is your FastAPI application instance.
# Everything hangs off this object.
app = FastAPI(title="Voizegen API", version="1.0.0")

# This is your first endpoint — a health check.
# When the frontend (or anyone) hits GET /health, it gets {"status": "ok"} back.
# This is standard practice to confirm the server is running.
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Voizegen backend is running"}