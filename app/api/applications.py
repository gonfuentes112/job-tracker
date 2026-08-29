from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.application import Application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_application = Application(
        company=application.company,
        role=application.role,
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get("/", response_model=list[ApplicationResponse])
def list_applications(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    applications = db.scalars(select(Application)).all()

    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.scalar(select(Application).where(Application.id == application_id))

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.patch(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.scalar(select(Application).where(Application.id == application_id))

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    update_data = application_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


@router.delete(
    "/{application_id}",
    status_code=204,
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.scalar(select(Application).where(Application.id == application_id))

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return {"message": "Application deleted"}
