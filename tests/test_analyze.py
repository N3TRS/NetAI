from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from groq import APIError
from app.main import app

client = TestClient(app)

MOCK_ANALYSIS = "## Lenguaje detectado\nPython\n\n## Errores y problemas encontrados\nNo se encontraron errores."
VALID_PAYLOAD = {"prompt": "¿Qué hace este código?", "code": "def suma(a, b):\n    return a + b"}


def test_analyze_success():
    with patch("app.analysis.chatAnalysis.chatAnalysis", return_value=MOCK_ANALYSIS):
        response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "analysis": MOCK_ANALYSIS}


def test_analyze_empty_code_returns_422():
    response = client.post("/analyze", json={"prompt": "¿Qué hace esto?", "code": ""})
    assert response.status_code == 422
    assert "código" in response.json()["detail"].lower()


def test_analyze_whitespace_code_returns_422():
    response = client.post("/analyze", json={"prompt": "¿Qué hace esto?", "code": "   "})
    assert response.status_code == 422


def test_analyze_empty_prompt_returns_422():
    response = client.post("/analyze", json={"prompt": "", "code": "print('hola')"})
    assert response.status_code == 422
    assert "solicitud" in response.json()["detail"].lower()


def test_analyze_whitespace_prompt_returns_422():
    response = client.post("/analyze", json={"prompt": "  ", "code": "print('hola')"})
    assert response.status_code == 422


def test_analyze_groq_api_error_returns_503():
    mock_request = MagicMock()
    mock_error = APIError("service unavailable", request=mock_request, body={})
    with patch("app.analysis.chatAnalysis.chatAnalysis", side_effect=mock_error):
        response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 503


def test_analyze_unexpected_error_returns_500():
    with patch("app.analysis.chatAnalysis.chatAnalysis", side_effect=RuntimeError("boom")):
        response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 500


def test_analyze_missing_fields_returns_422():
    response = client.post("/analyze", json={"prompt": "hola"})
    assert response.status_code == 422
