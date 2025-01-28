from fastapi import HTTPException

import azure.cognitiveservices.speech as speechsdk
from xml.sax.saxutils import escape
from api.models.synthesis_request import SynthesisRequest


class SpeechService:
    def __init__(self, settings):
        self.settings = settings

    def synthesize_speech(self, request: SynthesisRequest):
        """
        Convierte texto a voz usando Azure Cognitive Services

        Devuelve un archivo de audio MP3 con el texto sintetizado
        """
        try:
            # Configuración del servicio de voz
            speech_config = speechsdk.SpeechConfig(
                subscription=self.settings.AZURE_SPEECH_KEY,
                region=self.settings.AZURE_SPEECH_REGION,
            )

            # Configurar voz y formato de salida
            voice_name = request.voice_name or self.settings.DEFAULT_VOICE
            speech_config.speech_synthesis_voice_name = voice_name

            output_format = getattr(
                speechsdk.SpeechSynthesisOutputFormat,
                request.output_format or self.settings.OUTPUT_FORMAT,
            )
            speech_config.set_speech_synthesis_output_format(output_format)

            # Generar SSML con la estructura correcta
            ssml_rate = f"{int(request.rate * 100)}%"
            escaped_text = escape(request.text)
            ssml = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='es-CO'>
                <voice name='{voice_name}'>
                    <prosody rate='{ssml_rate}'>{escaped_text}</prosody>
                </voice>
            </speak>"""

            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, audio_config=None
            )

            result = synthesizer.speak_ssml_async(ssml).get()

            # Manejar resultados
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return result.audio_data

            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg = f"Síntesis cancelada: {cancellation.reason}"
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_msg += f" | Detalles: {cancellation.error_details}"
                raise HTTPException(status_code=500, detail=error_msg)

            raise HTTPException(
                status_code=500, detail="Error desconocido en la síntesis de voz"
            )

        except AttributeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de salida inválido: {request.output_format}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error en el servidor: {str(e)}"
            )
