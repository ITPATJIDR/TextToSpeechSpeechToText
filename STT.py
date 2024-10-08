import speech_recognition as sr
import os
from datetime import datetime
import wave

def save_audio_file(audio_data, file_path):
    # Save the audio file in WAV format
    with wave.open(file_path, "wb") as f:
        f.setnchannels(1)  # Mono channel
        f.setsampwidth(audio_data.sample_width)
        f.setframerate(audio_data.sample_rate)
        f.writeframes(audio_data.get_wav_data())

def speech_to_text():
    # Create directories if they don't exist
    os.makedirs("audio", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Initialize recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak...")
        audio = recognizer.listen(source)

    try:
        # Convert speech to text using Google's speech recognition
        # text = recognizer.recognize_google(audio, language="th-TH")
        text = recognizer.recognize_google(audio)
        print(f"Recognized Text: {text}")

        # Get current time for file naming
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save audio file to audio directory
        audio_file_path = f"audio/audio_{current_time}.wav"
        save_audio_file(audio, audio_file_path)
        print(f"Audio saved to {audio_file_path}")

        # Save the text to the outputs directory
        text_file_path = f"outputs/speech_output_{current_time}.txt"
        with open(text_file_path, "w") as file:
            file.write(text)
            print(f"Text saved to {text_file_path}")

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Error: Could not request results from the recognition service.")

if __name__ == "__main__":
    speech_to_text()
