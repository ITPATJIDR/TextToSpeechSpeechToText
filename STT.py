import speech_recognition as sr
import os
from datetime import datetime
from enum import Enum
import wave

import whisper      # pip install openai-whisper


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
    os.makedirs("output", exist_ok=True)

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
        audio_file_path = f"audio/audio_stt_{current_time}.wav"
        save_audio_file(audio, audio_file_path)
        print(f"Audio saved to {audio_file_path}")

        # Save the text to the output directory
        text_file_path = f"output/speech_stt_output_{current_time}.txt"
        with open(text_file_path, "w") as file:
            file.write(text)
            print(f"Text saved to {text_file_path}")

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Error: Could not request results from the recognition service.")



class WhisperModel(Enum):
    TINY = "tiny"           # params 39M | req VRAM ~ 1 GB | EN only 
    BASE = "base"           # params 74M | req VRAM ~ 1 GB | EN only
    SMALL = "small"         # params 244M | req VRAM ~ 2 GB | EN only
    MEDIUM = "medium"       # params 769M | req VRAM ~ 5 GB | EN only
    LARGE = "large"         # params 1550M | req VRAM ~ 10 GB
    TURBO = "turbo"         # params 809M | req VRAM ~ 6 GB
    # ref.md for more details 

def whisper_to_text(audio_file_path=None, save_record_audio=True, model:WhisperModel=WhisperModel.BASE):
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # create whisper model instance
    model = whisper.load_model(model.value)
    
    if (audio_file_path):
        # import audio file
        result = model.transcribe(audio_file_path)
        
    else:
        # record audio
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("\nPlease speak...")
            recorded_audio = recognizer.listen(source)
        
        recorded_audio_file_path = f"audio/stt_recorded_{dt}.wav"
        save_audio_file(recorded_audio, recorded_audio_file_path)
        
        # transcribe audio
        result = model.transcribe(recorded_audio_file_path)
        
        if (not save_record_audio):
            os.remove(recorded_audio_file_path)
            
    # print result
    print(f"\nRecognized Text: {result}")
    
    # save the result to a text transcription file
    output_file_path = f"output/stt_whisper_output_{dt}.txt"
    with open(output_file_path, "w") as file:
        file.write(result)
        print(f"Text saved to {output_file_path}")
    
    ...



if __name__ == "__main__":
    # speech_to_text()
    # whisper_to_text(model=WhisperModel.MEDIUM)
    whisper_to_text(audio_file_path="audio/tts_output_20241010_032241.mp3")
