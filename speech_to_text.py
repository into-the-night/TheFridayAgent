import pyaudio
import wave
import time
from faster_whisper import WhisperModel

model_size = "large-v3"


def get_speech():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input = True, frames_per_buffer=1024)

    flag = True
    frames = []
    start = time.time()
    print("start")
    while flag:
        if ((time.time()-start) > 5):
            flag = False
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open("speech.wav","wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe("speech.wav", beam_size=5)
    text = ''
    for segment in segments:
        text += segment.text
    return text