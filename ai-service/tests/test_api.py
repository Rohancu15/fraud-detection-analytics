import json
import pytest

from app import app


# =========================================================
# 🔹 Pytest Client
# =========================================================
@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# =========================================================
# 🔹 Mock Groq Response
# =========================================================
@pytest.fixture
def mock_groq(monkeypatch):

    def mock_generate_response(prompt):

        return json.dumps({
            "risk_level": "High",
            "explanation": "Suspicious activity detected",
            "key_indicators": [
                "Multiple countries",
                "Rapid transactions"
            ]
        })

    monkeypatch.setattr(
        "routes.describe.generate_response",
        mock_generate_response
    )


# =========================================================
# 1. Test /health
# =========================================================
def test_health(client):

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"


# =========================================================
# 2. Test /describe success
# =========================================================
def test_describe_success(client, mock_groq):

    response = client.post(
        "/describe",
        json={
            "text": "Suspicious transaction activity"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"

    assert "data" in data

    assert "risk_level" in data["data"]


# =========================================================
# 3. Test /describe missing text
# =========================================================
def test_describe_missing_text(client):

    response = client.post(
        "/describe",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"


# =========================================================
# 4. Test /recommend success
# =========================================================
def test_recommend_success(client):

    response = client.post(
        "/recommend",
        json={
            "text": "Multiple failed logins"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"

    assert isinstance(data["data"], list)


# =========================================================
# 5. Test /recommend missing text
# =========================================================
def test_recommend_missing_text(client):

    response = client.post(
        "/recommend",
        json={}
    )

    assert response.status_code == 400


# =========================================================
# 6. Test /generate-report success
# =========================================================
def test_generate_report_success(client, monkeypatch):

    def mock_report(prompt):

        return json.dumps({
            "title": "Fraud Report",
            "executive_summary": "Summary",
            "overview": "Overview",
            "top_items": ["item1"],
            "recommendations": ["rec1"]
        })

    monkeypatch.setattr(
        "routes.describe.generate_response",
        mock_report
    )

    response = client.post(
        "/generate-report",
        json={
            "text": "Fraud activity"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"

    assert "title" in data["data"]


# =========================================================
# 7. Test /generate-report missing text
# =========================================================
def test_generate_report_missing_text(client):

    response = client.post(
        "/generate-report",
        json={}
    )

    assert response.status_code == 400


# =========================================================
# 8. Test /analyse-document success
# =========================================================
def test_analyse_document_success(client, monkeypatch):

    def mock_analysis(prompt):

        return json.dumps({
            "summary": "Suspicious document",
            "risks": [
                "Money laundering"
            ],
            "key_findings": [
                "Multiple countries"
            ]
        })

    monkeypatch.setattr(
        "routes.describe.generate_response",
        mock_analysis
    )

    response = client.post(
        "/analyse-document",
        json={
            "text": "Large international transfers"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"

    assert "summary" in data["data"]


# =========================================================
# 9. Test /analyse-document missing text
# =========================================================
def test_analyse_document_missing_text(client):

    response = client.post(
        "/analyse-document",
        json={}
    )

    assert response.status_code == 400


# =========================================================
# 10. Test invalid endpoint
# =========================================================
def test_invalid_endpoint(client):

    response = client.get("/invalid-route")

    assert response.status_code in [404, 500]