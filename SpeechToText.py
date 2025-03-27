# Library for speech to text conversion
import speech_recognition as sr

# Library for file handling
from os import path

# Set properties for the speech recognition
nome_file = "./output/transcription.txt"

recognizer = sr.Recognizer()
audio_file = path.join(path.dirname(path.realpath(__file__)), "./input/audio.wav")
with sr.AudioFile(audio_file) as source:
    audio = recognizer.record(source)

try:
    with open(nome_file, "w") as file:
        # Convert audio to text
        file.write(recognizer.recognize_google(audio))

except sr.UnknownValueError:
    print("I could not understand audio")
except sr.RequestError as e:
    print("SpeechRecognition error; {0}".format(e))
