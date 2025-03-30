# Library for speech to text conversion
import speech_recognition as sr

# Library for file handling
from os import path, remove
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

def process_chunk(chunk, idx):
    chunk_filename = f"./input/audio_chunk_{idx}.wav"
    chunk.export(chunk_filename, format="wav")
    print(f"Exported {chunk_filename}")

    with sr.AudioFile(chunk_filename) as source:
        audio = recognizer.record(source)

    try:
        transcription = recognizer.recognize_google(audio)
        return f"\n{transcription}\n"
    except sr.UnknownValueError:
        return f"Could not understand audio\n"
    except sr.RequestError as e:
        return f"Chunk {idx}: API error: {e}\n"

recognizer = sr.Recognizer()
audio_file = path.join(path.dirname(path.realpath(__file__)), "./input/audio.wav")

#Check the size of the audio_file
if path.getsize(audio_file) == 0:
    print("Audio file is empty")
    exit()
# Divide the audio file into smaller chunks
elif path.getsize(audio_file) > 100:
    print("Audio file is too large")
    
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export("output/converted_audio.wav", format="wav")
    audio = AudioSegment.from_wav("output/converted_audio.wav")

    # Define chunk duration in milliseconds (1 minute)
    chunk_duration = 60 * 1000 
    chunks = [audio[i:i + chunk_duration] for i in range(0, len(audio), chunk_duration)]

    # Process chunks in parallel
    transcriptions = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_chunk, chunks, range(len(chunks)))
        transcriptions.extend(results)

    # Write all transcriptions to the file at once
    with open("./output/transcription.txt", "w") as file:
        file.writelines(transcriptions)

    # delete every chunck file created
    for i in range(len(chunks)):
        chunk_filename = f"./input/audio_chunk_{i}.wav"
        if path.exists(chunk_filename):
            remove(chunk_filename)
    print("Transcription complete")
