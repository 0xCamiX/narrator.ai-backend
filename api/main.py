from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.text_to_speech import router as tts_router

app = FastAPI(title="Azure Text-to-Speech API")

# Configuración CORS (ajustar según necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
async def health_check():
    """Endpoint de verificación de estado"""
    return {"status": "ok", "service": "Azure Text-to-Speech API"}


app.include_router(tts_router, prefix="/speech", tags=["Synthesis"])
