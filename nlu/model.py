
import yaml
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
from keras.utils import to_categorical



data = yaml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())

inputs, outputs = [], []

for command in data['commands']:
    inputs.append(command['input'].lower()) #diz os comandos escritos no train.yml
    outputs.append('{}\{}'.format(command['entity'], command['action']))

# processar texto: palavras, caracteres, bytes, sub-palavras

chars = set()
for input in inputs + outputs:
    for ch in input:
        if ch not in chars:
            chars.add(ch)

#Mapear chars-index

chr2idx = {} #criando minha base de dicionario -> caracteres
idx2chr = {} #criando minha base de dicionario -> numero

for i, ch in enumerate(chars):
    chr2idx[ch] = i
    idx2chr[i] = ch


max_seq = max([len(x) for x in inputs])

print('Número de chars:', len(chars))
print('Maior seq:', max_seq)

#criar o dataset one-hot (número de exemplos, tamanho da sequência, número de caracteres)
#criar datasex disperso (número de exemplos, tamanho da sequência_
input_data = np.zeros((len(inputs), max_seq, len(chars)), dtype='int32')

#Criar labels para o classificador

labels = set(outputs)
labels2idx = {}
idx2lbel = {}

for k, label in enumerate(labels):
    labels2idx[label] = k
    idx2lbel[k] = label

output_data = []

for output in outputs:
    output_data.append(labels2idx[output])

output_data = to_categorical(output_data, len(output_data))

for i, input in enumerate(inputs):
    for k, ch in enumerate(input):
        input_data[i, k, chr2idx[ch]] = 1.0

print(output_data[0])

model = Sequential()
model.add(Embedding(len(chars), 128))
model.add(LSTM(128))
model.add(Dense(len(output_data), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc']) 
model.summary()


'''
print(inputs)
print(outputs)
'''