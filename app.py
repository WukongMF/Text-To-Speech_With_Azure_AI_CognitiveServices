from flask import Flask, render_template, request, jsonify
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__)

# Define your Azure key and region
key = "4079e6ad450e4b1cb3d4437eb437c066"  # Replace with your actual Azure API key
service_region = "centralus"  # Replace with your actual service region

def get_available_voices(language):
    # Get the list of available voices for the given language
    speech_config = speechsdk.SpeechConfig(subscription=key, region=service_region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    voices = synthesizer.get_voices_async().get().voices
    return [voice for voice in voices if voice.locale.startswith(language)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_voices', methods=['POST'])
def get_voices():
    language = request.form['language']
    available_voices = get_available_voices(language)
    voices_list = [{'short_name': voice.short_name, 'local_name': voice.local_name} for voice in available_voices]
    return jsonify(voices_list)

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    voice_name = request.form['voice_name']
    rate = request.form['rate']

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

    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    # Handle the results
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return jsonify({'status': 'success', 'message': f"Speech synthesized to [{output_filename}] for text [{text}] with voice [{voice_name}]"})
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        return jsonify({'status': 'error', 'message': f"Speech synthesis canceled: {cancellation_details.reason}"})

if __name__ == '__main__':
    app.run(debug=True)