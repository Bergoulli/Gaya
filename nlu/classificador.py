import numpy as np
from keras.models import load_model

# Configurações
max_seq_length = 48
num_chars = 256

#CARREGAMENTO E PROCESSAMENTO DE DADOS

def load_labels(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        labels = [line.strip() for line in file]
    return labels

#CLASSIFCAÇÃO DE TEXTO

def classify(model, labels, text):
    x = np.zeros((1, max_seq_length, num_chars), dtype='float32')
    for k, ch in enumerate(bytes(text.encode('utf-8'))):
        x[0, k, int(ch)] = 1.0

    out = model.predict(x)
    idx = out.argmax()
    return labels[idx]

# AREA PARA TESTE SE ESTÁ OCORRENDO TUDO BEM

model = load_model('model.hdf5', compile=False)
labels = load_labels('labels.txt')

while True:
    res = input('Digite um texto: ')
    entity = classify(model, labels, res)
    print(entity)
