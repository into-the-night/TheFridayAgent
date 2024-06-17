from dotenv import load_dotenv
import os
load_dotenv()

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
access_key = os.getenv("PVPORCUPINE_ACCESS_KEY")

import pvporcupine
import pyaudio
import numpy as np
import speech_recognition as sr
from AppOpener import open
from speech_to_text import get_speech


porcupine = pvporcupine.create(
    access_key=access_key,
    keyword_paths=["Hey-Friday_en_windows_v3_0_0.ppn"],
    # model_path="porcupine_params_ja.pv"
)

pa = pyaudio.PyAudio()


def audio_callback(in_data, frame_count, time_info, status):

    pcm = np.frombuffer(in_data, dtype=np.int16)
    result = porcupine.process(pcm)
    
    if result >= 0:
        open("whatsapp")
        text = get_speech()
        print(text)

    return (in_data, pyaudio.paContinue)

stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate= porcupine.sample_rate,
    input=True,
    frames_per_buffer=porcupine.frame_length,
    stream_callback= audio_callback
    )

print("I am listening...")
stream.start_stream()

try:
    while True:
        pass
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
