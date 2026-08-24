from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database": settings.postgres_db,
    }


# if __name__ == "__main__":
#     main()
