from pydantic import BaseModel, Field


class SynthesisRequest(BaseModel):
    """Modelo de solicitud para síntesis de voz"""

    text: str = Field(..., min_length=1, example="Texto a convertir en voz")
    voice_name: str = Field(None, example="es-CO-SalomeNeural")
    output_format: str = Field(None, example="Audio16Khz32KBitRateMonoMp3")
    rate: float = Field(
        1.0,
        ge=0.2,
        le=2.0,
        description="Velocidad de habla (0.5 = 50% más lento, 2.0 = 100% más rápido)",
    )
