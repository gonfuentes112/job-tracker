from fastapi import FastAPI
from app.api.applications import router as applications_router
from app.core.config import settings
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
)

app = FastAPI()

app.include_router(applications_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database": settings.postgres_db,
    }


@app.post(
    "/applications",
    response_model=ApplicationResponse,
)
def create_application(
    application: ApplicationCreate,
):
    pass


# if __name__ == "__main__":
#     main()
