import os

os.environ["DEMO_MODE"] = "true"

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "LegalEase"
    assert data["status"] == "running"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_generate_document():

    payload = {
        "document_type": "Freelance Work Contract",
        "parties": (
            "Jane Doe (Freelancer), "
            "TechNova Inc. (Client)"
        ),
        "terms": (
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Work must be delivered by the agreed deadline"
        ),
        "effective_date": "2026-09-26",
        "jurisdiction": "Kerala, India",
        "language": "English",
    }

    response = client.post(
        "/generate",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert len(data["document"]) > 50


def test_generate_missing_parties():

    payload = {
        "document_type": "NDA",
        "parties": "",
        "terms": "Confidentiality applies",
        "effective_date": "2026-09-26",
        "jurisdiction": "Kerala, India",
        "language": "English",
    }

    response = client.post(
        "/generate",
        json=payload
    )

    assert response.status_code == 422