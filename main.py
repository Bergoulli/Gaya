from vosk import Model, KaldiRecognizer
import psutil
import os
import pyaudio
import pyttsx3
import json
import core
from nlu.classificador import classify
from keras.models import load_model
import subprocess
import webbrowser
import platform

# Inicialização da síntese de fala
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

def evaluate(text):
    entity = classify(model_keras, labels, text)
    
    if entity == 'time/getTime':
        fala(core.SystemInfo.get_time())
    elif entity == 'time/getDate':
        fala(core.SystemInfo.get_date())
    
    # Conversa
    if entity == 'fala/normal':
        fala('oi, como vai mestre?')

    # Abrir programas
    if entity == 'open/notas':
        fala('Ok mestre, abrindo o bloco de notas')
        os.system('notepad.exe')
    elif entity == 'open/brave':
        fala('Ok mestre, abrindo o brave')
        webbrowser.open('https://www.google.com.br/?hl=pt-BR')
    elif entity == 'open/sigaa':
        fala('Ok mestre, abrindo o sigaa')
        webbrowser.open('https://si3.ufc.br/sigaa/verTelaLogin.do')
    elif entity == 'open/insta':
        fala('Ok mestre, abrindo o instagram')
        webbrowser.open('https://www.instagram.com/')
    elif entity == 'open/insta':
        fala('Ok mestre, abrindo o youtube')
        webbrowser.open('https://www.youtube.com/')
    elif entity == 'open/so':
        fala('Mestre, seu sistema operacional é')
        print(platform.platform())
    elif entity == 'open/process':
        fala('Mestre, seu processador é')
        print(platform.processor())
    elif entity == 'open/bit':
        fala('Mestre, seu sistema de bits é')
        print(platform.machine())

    print(f'tipo: {entity}')

def close_program(name):
    for process in (process for process in psutil.process_iter() if process.name() == name):
        process.kill()

model = Model('model')
labels = load_labels('labels.txt')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

model_keras = load_model('model.hdf5', compile=False)

# Loop do reconhecimento de fala

while True:
    data = stream.read(4048)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)
        text = result['text']
        print(text)

        if text == 'gaia desligar':
            break

        elif result is not None and 'gaia' in text:
            evaluate(text)
