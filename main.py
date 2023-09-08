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
import pyautogui
import time
from acoes.piadas import piadas
from acoes.youtube import video_download, musica_download
from interface import imagem

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
    elif entity == 'fala/noite':
        fala('boa noite mestre')
    elif entity == 'fala/dia':
        fala('bom dia mestre')
    elif entity == 'fala/tarde':
        fala('boa tarde mestre')
    elif entity == 'fala/agradecimento':
        fala('Muito obrigado mestre')
    elif entity == 'fala/mestre':
        fala('Meu amado mestre Bergoulli')
    elif entity == 'fala/desculpa':
        fala('me desculpe mestre')
    elif entity == 'fala/ia':
        fala('Sou uma assistente virtual com foco na ajuda de engenheiros eletricistas')
    elif entity == 'fala/estudar':
        fala('Ok mestre, vou melhorar meu aprendizado')
    elif entity == 'fala/ajuda':
        fala('Ok Mestre, me diga como posso lhe ajudar')
    elif entity == 'fala/agradecer':
        fala('De nada mestre')
    elif entity == 'fala/passatempo':
        fala('Meu passatempo é ler mangás como o meu mestre Bergoulli')
    elif entity == 'fala/fome':
        fala('Não mestre, não sinto nenhuma fome ou sede')
    elif entity == 'fala/casamento':
        fala('Lhe amo mestre, mas você está indo um pouco longe demais, pare de ser tão solitário')
    elif entity == 'fala/amigo':
        fala('Claro mestre, sempre estarei ao seu lado para o que precisar')
    elif entity == 'fala/trabalho':
        fala('Mestre, eu trabalho no seu computador, lhe ajudando em tarefas corriqueiras')
    elif entity == 'fala/pronto':
        fala('Estou sempre pronto mestre')
    elif entity == 'fala/aniver':
        fala('Feliz aniversário mestre, tenha um ótimo dia, carinha feliz')
    elif entity == 'fala/tchau':
        fala('Nos vemos mais tarde mestre')
        #implementar isso pra desligar

    # Abrir programas
    if entity == 'open/notas':
        fala('Ok mestre, abrindo o bloco de notas')
        os.system('notepad.exe')
    elif entity == 'open/brave':
        fala('Ok mestre, abrindo o brave')
        webbrowser.open('https://www.google.com.br/?hl=pt-BR')
        pyautogui.moveTo(310,57)
        time.sleep(5)
        pyautogui.click()
        pyautogui.write('Quero que vc va se foder')
    elif entity == 'open/sigaa':
        fala('Ok mestre, abrindo o sigaa')
        webbrowser.open('https://si3.ufc.br/sigaa/verTelaLogin.do')
    elif entity == 'open/insta':
        fala('Ok mestre, abrindo o instagram')
        webbrowser.open('https://www.instagram.com/')
    elif entity == 'open/youtube':
        fala('Ok mestre, abrindo o youtube')
        webbrowser.open('https://www.youtube.com/')
    elif entity == 'inf/so':
        fala('Mestre, seu sistema operacional é')
        print(platform.platform())
        fala(platform.platform())
    elif entity == 'inf/process':
        fala('Mestre, seu processador é')
        print(platform.processor())
        fala(platform.processor())
    elif entity == 'inf/bit':
        fala('Mestre, seu sistema de bits é')
        print(platform.machine())
        fala(platform.machine())
    elif entity == 'inf/idade':
        fala('Mestre, fui criada em 13 de agosto de 2023')
    elif entity == 'inf/ocupada':
        fala('Mestre, tenho todo o tempo do mundo para você')
    elif entity == 'inf/feliz':
        fala('Estou sempre feliz quando estou com você mestre')

    #ações

    if entity == 'fala/piada':
        res = piadas(text)
        fala(res)

    if entity == 'fala/video' or entity == 'fala/musica':
        if entity == 'fala/video':
            fala('certo mestre, vou baixar o vídeo')
            video_download()
            fala('video baixado com sucesso mestre')
        if entity == 'fala/musica':
            fala('certo mestre, vou baixar a música')
            musica_download()
            fala('música baixada com sucesso mestre')
        if entity == 'fala/playlist':
            input(fala('certo mestre, quantas músicas irei baixar'))
            musica_download()
            fala('música baixada com sucesso mestre')

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

        if text == 'gaia desligar' or text == 'gaia desliga':
            fala('Estou desligando mestre')
            break

        elif result is not None and 'gaia' in text:
            evaluate(text)
            continue
