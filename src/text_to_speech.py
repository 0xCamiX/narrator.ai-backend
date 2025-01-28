"""
For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk
"""

import os
import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = "eastus2"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
# speech_config.speech_synthesis_voice_name = "en-US-BrandonMultilingualNeural"
speech_config.speech_synthesis_voice_name = "es-CO-SalomeNeural"

text = """¿Necesitas una ventilación eficiente y controlar la humedad excesiva en tu fábrica, bodega o casa? Tenemos la solución ideal sin costos de energía eléctrica, funcionando las 24 horas del día.
Los extractores eólicos ofrecen un ambiente más saludable, libre de polución suspendida en el aire, y reducen el calor al utilizar el viento para mover su turbina de succión.
Fabricados con aluminio templado H14, estos equipos no se oxidan y tienen una vida útil de hasta 40 años, con prácticamente cero mantenimiento.
¡Contáctanos al 317 752 5559 para más información!"""

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

result = speech_synthesizer.speak_text_async(text).get()
# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
    # Save the audio to a file
    audio_stream = speechsdk.AudioDataStream(result)
    file_path = "output_audio.mp3"
    audio_stream.save_to_wav_file(file_path)
    print(f"Audio content saved to file: {file_path}")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
