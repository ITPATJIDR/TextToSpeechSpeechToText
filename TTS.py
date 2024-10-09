import os
from datetime import datetime
from pathlib import Path
import pyttsx3

from gtts import gTTS       # pip install gtts || pip install google-cloud-speech
# from playsound import playsound            # pip install playsound (available on Python 3.9 and below)


def text_to_speech(file_path):
    # Initialize TTS engine
    engine = pyttsx3.init()

    # Read text from file
    with open(file_path, "r") as file:
        text = file.read()

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()


def text_to_speech_google(text=None, file=None, lang="en", save_audio=True):
    # Initialize TTS engine
    if (text is None and file is None):
        print("Please provide either text or file path.")
        return
    elif (text):
        tts = gTTS(text=text, lang=lang)
    elif (file):
        with open(file, "r") as f:
            text = f.read()
        tts = gTTS(text=text, lang=lang)
    
    
    # Create directories if they don't exist
    os.makedirs("audio", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Get current time for file naming
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path(__file__).resolve().parents[0]
    audio_file_path = base_dir / f"audio/tts_output_{dt}.mp3"
    audio_file_path_str = str(audio_file_path)
    print(f"\nSaving audio to {audio_file_path}\n")
    
    # Perform Save the audio file
    tts.save(audio_file_path)
    os.system(audio_file_path_str)

    # delete the audio file after playing sound
    if (not save_audio):
        os.remove(audio_file_path)
        
    

if __name__ == "__main__":
    file = "./output/speech_output_20241008_213109.txt"
    # text_to_speech(file)
    
    # new text to speech from gTTS (Google Text To Speech)
    text_to_speech_google(text="Come!, into the unknown")
    text_to_speech_google(file=file)
    text_to_speech_google(text="Haiya! Mr. Roger don't like this MSG", save_audio=False)
    