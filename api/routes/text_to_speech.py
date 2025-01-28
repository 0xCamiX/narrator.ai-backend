from fastapi import APIRouter, HTTPException, Response, Depends
from api.models.synthesis_request import SynthesisRequest
from api.services.speech_service import SpeechService
from pydantic_settings import BaseSettings

router = APIRouter()


class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno"""

    AZURE_SPEECH_KEY: str
    AZURE_SPEECH_REGION: str = "eastus2"
    DEFAULT_VOICE: str = "es-CO-SalomeNeural"
    OUTPUT_FORMAT: str = "Audio16Khz32KBitRateMonoMp3"

    class Config:
        env_file = ".env"


def get_settings():
    """Obtener la configuración de la aplicación"""
    return Settings()


@router.post("/synthesize")
def synthesize_speech(
    request: SynthesisRequest, settings: Settings = Depends(get_settings)
):
    service = SpeechService(settings)
    try:
        audio_data = service.synthesize_speech(request)
        headers = {"Content-Disposition": "attachment; filename=speech.mp3"}
        return Response(content=audio_data, media_type="audio/mpeg", headers=headers)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
