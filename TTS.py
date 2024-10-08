import pyttsx3

def text_to_speech(file_path):
    # Initialize TTS engine
    engine = pyttsx3.init()

    # Read text from file
    with open(file_path, "r") as file:
        text = file.read()

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()

text_to_speech("./outputs/speech_output_20241008_213109.txt")
