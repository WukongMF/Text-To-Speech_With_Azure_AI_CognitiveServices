import azure.cognitiveservices.speech as speechsdk

# Define your Azure key and region
key = "4079e6ad450e4b1cb3d4437eb437c066"  # Replace with your actual Azure API key
service_region = "centralus"  # Replace with your actual service region

def text_to_speech(text: str, voice_name: str, rate: str = "0%"):
    # Configure Azure Speech Service
    speech_config = speechsdk.SpeechConfig(subscription=key, region=service_region)
    speech_config.speech_synthesis_voice_name = voice_name

    # Set up the audio output configuration
    output_filename = f"{voice_name}.wav"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)

    # Create the SSML with the desired rate
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='{voice_name}'>
            <prosody rate='{rate}'>
                {text}
            </prosody>
        </voice>
    </speak>"""

    # Create the speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    print(f"Converting text to speech with voice '{voice_name}' at rate '{rate}': '{text}'")
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    # Handle the results
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized to [{output_filename}] for text [{text}] with voice [{voice_name}]")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
            print("Did you set up the speech resource key and region values correctly?")

def get_available_voices(language):
    # Get the list of available voices for the given language
    speech_config = speechsdk.SpeechConfig(subscription=key, region=service_region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    voices = synthesizer.get_voices_async().get().voices
    return [voice for voice in voices if voice.locale.startswith(language)]

# Solicitar el texto al usuario
text = input("Introduce el texto que quieres convertir a voz: ")

# Solicitar el idioma y variante
languages = {
    "1": "es",
    "2": "en",
    "3": "fr"
}

print("Selecciona el idioma y variante:")
print("1: Español")
print("2: Inglés")
print("3: Francés")
language_choice = input("Introduce el número del idioma seleccionado: ")

if language_choice in languages:
    language = languages[language_choice]
    available_voices = get_available_voices(language)
    print("Selecciona la variante de voz:")
    for idx, voice in enumerate(available_voices):
        print(f"{idx + 1}: {voice.short_name} - {voice.local_name}")
    voice_choice = int(input("Introduce el número de la variante de voz seleccionada: "))
    if 1 <= voice_choice <= len(available_voices):
        voice_name = available_voices[voice_choice - 1].short_name
        rate = input("Introduce la velocidad de la voz (por ejemplo, -10% para más lento, +10% para más rápido, 0% para velocidad normal): ")
        text_to_speech(text, voice_name, rate)
    else:
        print("Variante de voz no válida.")
else:
    print("Idioma no válido.")