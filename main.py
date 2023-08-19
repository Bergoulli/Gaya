from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json
import core
from nlu.classificador import classify
from keras.models import load_model

#sintese de fala
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-2].id)

def fala(text):
    engine.say(text)
    engine.runAndWait()

def load_labels(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        labels = [line.strip() for line in file]
    return labels

model = Model('model')
labels = load_labels('labels.txt')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

model_keras = load_model('model.hdf5', compile=False)

#loop do reconhecimento de fala
while True:
    data = stream.read(4048)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)

        if result is not None:
            text = result['text']
            entity = classify(model_keras, labels, text)


            if entity == 'time/getTime':
                fala(core.SystemInfo.get_time())
            
            print(f'texto: {text}, tipo: {entity}')


