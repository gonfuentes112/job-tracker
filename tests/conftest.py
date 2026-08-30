import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.dependencies import get_db
from app.db.base import Base
from app.core.config import settings

test_engine = create_engine(
    settings.test_database_url,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "password123",
    }


@pytest.fixture
def registered_user(client, user_data):
    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 200

    return user_data


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/auth/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture
def second_auth_headers(client):
    user = {
        "email": "second@example.com",
        "password": "password123",
    }

    response = client.post(
        "/auth/register",
        json=user,
    )

    assert response.status_code == 200

    response = client.post(
        "/auth/login",
        data={
            "username": user["email"],
            "password": user["password"],
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }
