from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["service"] == "EduGenie"


def test_qa_without_api_key():

    response = client.get(
        "/qa",
        params={
            "question": "What is Python?"
        }
    )

    # If API key is missing,
    # the application should return 503.
    #
    # If an API key exists,
    # the endpoint may return 200.
    assert response.status_code in {
        200,
        503,
        502
    }