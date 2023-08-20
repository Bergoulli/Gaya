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
    if entity == 'fala/normal2':
        fala('Vou bem mestre, obrigado?')

    # Abrir programas
    def open_program(program):
        subprocess.Popen([program], shell=True)

    if entity == 'open/notas':
        fala('Abrindo o bloco de notas')
        os.system('notepad.exe')
    elif entity == 'open/brave':
        fala('Abrindo o brave')
        webbrowser.open('https://www.google.com.br/?hl=pt-BR')
    elif entity == 'open/sigaa':
        fala('Abrindo o sigaa')
        webbrowser.open('https://si3.ufc.br/sigaa/verTelaLogin.do')
    elif entity == 'open/insta':
        fala('Abrindo o instagram')
        webbrowser.open('https://www.instagram.com/')
    
    # Fechar programas
    if entity == 'close/notas':
        fala('Fechando o bloco de notas')
        close_program('notepad.exe')

    print(f'texto: {text}, tipo: {entity}')

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

        if result is not None:
            text = result['text']
            evaluate(text)
