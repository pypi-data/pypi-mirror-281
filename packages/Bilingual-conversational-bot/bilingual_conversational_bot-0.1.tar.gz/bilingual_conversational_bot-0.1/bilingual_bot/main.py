# steps to Integrate this app with Microsoft teams 
# as we run this file select 
""" 
Local Machine Setting

Microphone :- Microphone Array (Realtek High
Speaker :- CABLE Input (VB-Audio Virtual C


Microsoft Teams Setting 
keep everything as it is only change 

Microphone :- Cable Output and aage jo bhi honga wo 

"""




import streamlit as st
import googletrans
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import time
import io

# Initialize speech recognition and translator objects
recognizer = sr.Recognizer()
translator = googletrans.Translator()

# Function to detect language and translate
def detect_and_translate(text):
    detected_lang = translator.detect(text).lang
    target_language = 'es' if detected_lang == 'en' else 'en'
    translation = translator.translate(text, dest=target_language)
    return translation.text, target_language

# Function to handle speech recognition, translation, and TTS
def recognize_and_translate(mic_index, speaker_index):
    conversation_active = True
    audio_interface = pyaudio.PyAudio()

    while conversation_active:
        try:
            # Open the selected microphone
            stream = audio_interface.open(format=pyaudio.paInt16,
                                          channels=1,
                                          rate=16000,
                                          input=True,
                                          input_device_index=mic_index,
                                          frames_per_buffer=1024)

            st.markdown('<div style="font-size: 24px; font-weight: bold; color: black;">Speak now...</div>', unsafe_allow_html=True)

            start_listen = time.time()
            frames = []

            # Capture audio data
            for _ in range(0, int(16000 / 1024 * 5)):  # 5 seconds of audio
                data = stream.read(1024)
                frames.append(data)

            end_listen = time.time()

            # Stop and close the stream
            stream.stop_stream()
            stream.close()

            # Convert audio frames to audio data
            audio_data = sr.AudioData(b''.join(frames), 16000, 2)

            # Recognize speech using Google Speech Recognition
            start_recognition = time.time()
            try:
                text = recognizer.recognize_google(audio_data, language='en-US')  # Try recognizing English speech
            except sr.UnknownValueError:
                text = recognizer.recognize_google(audio_data, language='es-ES')  # If fails, try recognizing Spanish speech
            end_recognition = time.time()
            st.markdown(f'<div style="padding: 10px; background-color: lightgreen;"><b>Recognized Text:</b> {text}</div>', unsafe_allow_html=True)

            # Detect language and translate
            start_translation = time.time()
            translated_text, target_language = detect_and_translate(text)
            end_translation = time.time()
            st.markdown(f'<div style="padding: 10px; background-color: lightgreen;"><b>Translated Text ({target_language}):</b> {translated_text}</div>', unsafe_allow_html=True)

            # Convert translated text to speech using gTTS
            start_tts = time.time()
            tts_audio = gTTS(text=translated_text, lang=target_language, slow=False)
            tts_audio_bytes = io.BytesIO()
            tts_audio.write_to_fp(tts_audio_bytes)
            tts_audio_bytes.seek(0)

            # Convert gTTS output to AudioSegment
            audio_segment = AudioSegment.from_file(tts_audio_bytes, format='mp3')

            # Play audio using specified output device (laptop speaker)
            stream_out = audio_interface.open(format=audio_interface.get_format_from_width(audio_segment.sample_width),
                                              channels=audio_segment.channels,
                                              rate=audio_segment.frame_rate,
                                              output=True,
                                              output_device_index=speaker_index)
            stream_out.write(audio_segment.raw_data)

            # Close the output stream
            stream_out.stop_stream()
            stream_out.close()

            end_tts = time.time()

            st.markdown('<div style="padding: 10px; background-color: lightblue; color: black;"><b>Time taken for listening:</b> {:.2f} seconds</div>'.format(end_listen - start_listen), unsafe_allow_html=True)
            st.markdown('<div style="padding: 10px; background-color: lightblue; color: black;"><b>Time taken for recognition:</b> {:.2f} seconds</div>'.format(end_recognition - start_recognition), unsafe_allow_html=True)
            st.markdown('<div style="padding: 10px; background-color: lightblue; color: black;"><b>Time taken for translation:</b> {:.2f} seconds</div>'.format(end_translation - start_translation), unsafe_allow_html=True)
            st.markdown('<div style="padding: 10px; background-color: lightblue; color: black;"><b>Time taken for TTS:</b> {:.2f} seconds</div>'.format(end_tts - start_tts), unsafe_allow_html=True)

        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            st.write(f"An error occurred: {e}")

        time.sleep(1)  # Delay before checking if conversation should continue

    st.write("Conversation stopped.")

# Function to list available audio devices
def list_audio_devices():
    audio_interface = pyaudio.PyAudio()
    devices = []
    for i in range(audio_interface.get_device_count()):
        device_info = audio_interface.get_device_info_by_index(i)
        devices.append((i, device_info['name']))
    audio_interface.terminate()
    return devices

# Function to find the index of the laptop speaker
def find_laptop_speaker_index(devices):
    for idx, name in devices:
        if 'speakers' in name.lower():
            return idx
    return None

# Streamlit UI
def main():
    st.title("Bilingual Conversation Bot")

    # List available microphones and speakers
    devices = list_audio_devices()
    mic_options = [device for device in devices if device[1].lower().startswith('microphone')]
    speaker_options = [device for device in devices if not device[1].lower().startswith('microphone')]

    # Find laptop speaker index (customize this logic based on your system)
    laptop_speaker_index = find_laptop_speaker_index(speaker_options)

    # Select microphone
    mic_index = st.selectbox("Select Microphone", mic_options, format_func=lambda x: x[1])[0]

    # Select speaker (use laptop speaker index if found, otherwise let the user select)
    speaker_index = st.selectbox("Select Speaker", speaker_options, index=laptop_speaker_index, format_func=lambda x: x[1])[0]

    # Create start button
    button_label = "Start Conversation"
    if st.button(button_label):
        st.write("Conversation started...")
        recognize_and_translate(mic_index, speaker_index)

if __name__ == "__main__":
    main()






















