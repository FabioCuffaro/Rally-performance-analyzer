"""Tests del Bloque 0 — verificación básica de la API."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_check_status_200():
    """El endpoint /health debe devolver 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_body():
    """El endpoint /health debe devolver status ok."""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "rally-performance-analyzer"


def test_docs_available():
    """Swagger UI debe estar disponible en /docs."""
    response = client.get("/docs")
    assert response.status_code == 200
