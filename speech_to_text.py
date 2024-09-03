import pyaudio
from faster_whisper import WhisperModel
import numpy as np
import io
import wave

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

CHANNELS = 1
model_size = "small"
THRESHOLD = 200
CHUNK = 1024
SILENCE_DURATION = 1.5
RATE = 44100

def is_silent(data):
    return np.abs(np.frombuffer(data, dtype=np.int16)).mean() < THRESHOLD


def get_speech():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input = True, frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if is_silent(data):
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open("speech.wav", 'wb') as sound_file:
        sound_file.setnchannels(CHANNELS)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(RATE)
        sound_file.writeframes(b''.join(frames))


    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe("speech.wav", beam_size=1 )
    text = ''
    for segment in segments:
        text += segment.text

    return text

print(get_speech())