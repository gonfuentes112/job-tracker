from fastapi import FastAPI
from app.api.applications import router as applications_router
from app.api.auth import router as auth_router

from sqlalchemy import text
from app.db.database import engine

app = FastAPI()

app.include_router(applications_router)
app.include_router(auth_router)


@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "ok",
    }
