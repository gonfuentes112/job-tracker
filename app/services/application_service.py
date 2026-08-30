from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.models.user import User


def create_application(
    application: ApplicationCreate, db: Session, current_user: User
) -> Application:
    new_application = Application(
        company=application.company,
        role=application.role,
        location=application.location,
        user_id=current_user.id,
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


def list_applications(db: Session, current_user: User) -> list[Application]:
    applications = db.scalars(
        select(Application).where(Application.user_id == current_user.id)
    ).all()

    return list(applications)


def get_application(
    application_id: int, db: Session, current_user: User
) -> Application:
    application = db.scalar(
        select(Application).where(
            Application.id == application_id, Application.user_id == current_user.id
        )
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session,
    current_user: User,
) -> Application:
    application = db.scalar(
        select(Application).where(
            Application.id == application_id, Application.user_id == current_user.id
        )
    )

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


def delete_application(application_id: int, db: Session, current_user: User):
    application = db.scalar(
        select(Application).where(
            Application.id == application_id, Application.user_id == current_user.id
        )
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return {"message": "Application deleted"}
