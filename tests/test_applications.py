def test_list_applications_requires_auth(client):
    response = client.get("/applications/")

    assert response.status_code == 401


def test_list_applications_requires_auth(client):
    response = client.get("/applications/")

    assert response.status_code == 401


def test_list_applications(client, auth_headers):
    client.post(
        "/applications/",
        json={
            "company": "Google",
            "role": "Software Engineer",
            "location": "Tokyo",
        },
        headers=auth_headers,
    )

    response = client.get(
        "/applications/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    applications = response.json()

    assert len(applications) == 1
    assert applications[0]["company"] == "Google"


def test_create_application_rejects_empty_location(
    client,
    auth_headers,
):
    response = client.post(
        "/applications/",
        json={
            "company": "Google",
            "role": "Software Engineer",
            "location": "",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_user_cannot_access_another_users_application(
    client,
    auth_headers,
    second_auth_headers,
):
    response = client.post(
        "/applications/",
        json={
            "company": "Google",
            "role": "Engineer",
            "location": "Tokyo",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    application_id = response.json()["id"]

    response = client.get(
        f"/applications/{application_id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404


def test_users_only_see_their_own_applications(
    client,
    auth_headers,
    second_auth_headers,
):
    # User 1 creates an application
    response = client.post(
        "/applications/",
        json={
            "company": "Google",
            "role": "Software Engineer",
            "location": "Tokyo",
        },
        headers=auth_headers,
    )

    assert response.status_code in (200, 201)

    # User 2 creates a different application
    response = client.post(
        "/applications/",
        json={
            "company": "Microsoft",
            "role": "Backend Engineer",
            "location": "Tokyo",
        },
        headers=second_auth_headers,
    )

    assert response.status_code in (200, 201)

    # User 1 requests their applications
    response = client.get(
        "/applications/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    applications = response.json()

    # User 1 should only see their own application
    assert len(applications) == 1
    assert applications[0]["company"] == "Google"
    assert applications[0]["role"] == "Software Engineer"

    # User 2 requests their applications
    response = client.get(
        "/applications/",
        headers=second_auth_headers,
    )

    assert response.status_code == 200

    applications = response.json()

    # User 2 should only see their own application
    assert len(applications) == 1
    assert applications[0]["company"] == "Microsoft"
    assert applications[0]["role"] == "Backend Engineer"
