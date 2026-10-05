from app.models.user import User
from app.core.security import verify_password
from app.core.dependencies import ALGORITHM, settings
from app.core.security import encode
from datetime import datetime, timezone, timedelta


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"


def test_duplicate_registration(client):
    data = {
        "email": "duplicate@example.com",
        "password": "password123",
    }

    first_response = client.post(
        "/auth/register",
        json=data,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/auth/register",
        json=data,
    )

    assert second_response.status_code == 400


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_register_stores_hashed_password(client, db):
    password = "password123"
    email = "hashcheck@example.com"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    user = db.query(User).filter(User.email == email).first()

    assert user is not None
    assert user.hashed_password != password
    assert verify_password(password, user.hashed_password)
    assert not verify_password("wrongpassword", user.hashed_password)


def test_expired_token_rejected(client, registered_user):
    expired_token = encode(
        {
            "sub": str(registered_user["id"]),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/applications",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401


def test_invalid_token_signature_rejected(client, registered_user):
    invalid_token = encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        "testing-an-incorrect-secret-to-validate",
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/applications",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 401


def test_invalid_user_id_in_token_rejected(client):
    invalid_token = encode(
        {
            "sub": "not-a-number",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/applications",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 401


def test_missing_sub_in_token_rejected(client):
    token = encode(
        {
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/applications",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_nonexistent_user_in_token_rejected(client):
    token = encode(
        {
            "sub": "999999999",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/applications",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_missing_authorization_header_rejected(client):
    response = client.get("/applications")

    assert response.status_code == 401
