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
