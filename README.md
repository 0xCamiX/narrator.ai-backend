# Azure Text-to-Speech API

Esta es una API de síntesis de texto a voz utilizando Azure Cognitive Services, construida con FastAPI.

## Requisitos

- Python 3.8+
- Azure Cognitive Services Speech SDK
- FastAPI
- Uvicorn

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/0xCamiX/narrator.ai-backend
    ```

2. Crea y activa un entorno virtual:

    ```sh
    pyenv virtualenv 3.13.1 relator-ai-env
    pyenv activate relator-ai-env
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Crea un archivo [.env](http://_vscodecontentref_/1) en el directorio `backend` con las siguientes variables de entorno:

    ```env
    AZURE_SPEECH_KEY=tu_azure_speech_key
    AZURE_SPEECH_REGION=tu_azure_speech_region
    ```

## Uso

1. Inicia la aplicación en desarrollo (en la carpeta raíz):

    ```sh
    fastapi dev api/main.py
    ```

2. La API debería estar en `http://localhost:8001` para no modificar el puerto del frontend.

## Endpoints

### Health Check

- **GET /**

    Verifica el estado del servicio.

    **Respuesta:**

    ```json
    {
        "status": "ok",
        "service": "Azure Text-to-Speech API"
    }
    ```

### Synthesize Speech

- **POST /speech/synthesize**

    Convierte texto a voz usando Azure Cognitive Services.

    **Cuerpo de la solicitud:**

    ```json
    {
        "text": "Texto a convertir en voz",
        "voice_name": "es-CO-SalomeNeural",
        "output_format": "Audio16Khz32KBitRateMonoMp3",
        "rate": 1.0
    }
    ```

    **Respuesta:**

    Retorna un archivo de audio MP3 con el texto sintetizado.

## Estructura del Proyecto

```plaintext
backend/
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── synthesis_request.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── text_to_speech.py
│   └── services/
│       ├── __init__.py
│       └── speech_service.py
└── .env
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia GNU General Pubic License V.3.0

