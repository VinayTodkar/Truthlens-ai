from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "TruthLens AI"
    assert data["status"] == "running"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_verify_without_input():

    response = client.post(
        "/api/v1/verify",
        json={}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Provide either text or URL."