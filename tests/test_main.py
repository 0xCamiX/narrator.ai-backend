import os
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def set_env_vars():
    os.environ["AZURE_SPEECH_KEY"] = os.getenv("AZURE_SPEECH_KEY")
    os.environ["AZURE_SPEECH_REGION"] = os.getenv("AZURE_SPEECH_REGION")
    yield
    del os.environ["AZURE_SPEECH_KEY"]
    del os.environ["AZURE_SPEECH_REGION"]


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Azure Text-to-Speech API"}


def test_synthesize_speech(set_env_vars):
    payload = {
        "text": "Hola, ¿cómo estás?",
        "voice_name": "es-CO-SalomeNeural",
        "output_format": "Audio16Khz32KBitRateMonoMp3",
        "rate": 1.0,
    }
    response = client.post("/speech/synthesize", json=payload)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/mpeg"
    assert "Content-Disposition" in response.headers
