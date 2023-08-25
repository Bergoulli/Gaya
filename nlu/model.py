import yaml
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.utils import to_categorical

# Configurações
max_seq_length = 48
num_chars = 256
num_epochs = 1024



#CARREGAMENTO E PROCESSAMENTO DE DADOS

def load_data(file_path):
    data = yaml.safe_load(open(file_path, 'r', encoding='utf-8').read())
    inputs, outputs = [], []

    for command in data['commands']:
        inputs.append(command['input'].lower())
        outputs.append('{}/{}'.format(command['entity'], command['action']))

    return inputs, outputs

def process_data(inputs, outputs):
    max_seq = max([len(bytes(x.encode('utf-8'))) for x in inputs])

    input_data = np.zeros((len(inputs), max_seq_length, num_chars), dtype='float32')  # Corrigido aqui
    for i, inp in enumerate(inputs):
        for k, ch in enumerate(bytes(inp.encode('utf-8'))):
            if k < max_seq_length:  # Garantir que não ultrapasse max_seq_length
                input_data[i, k, int(ch)] = 1.0
            else:
                break  # Parar de preencher quando atingir o comprimento máximo

    labels = set(outputs)
    label2idx = {label: idx for idx, label in enumerate(labels)}
    idx2label = {idx: label for label, idx in label2idx.items()}

    output_data = [label2idx[output] for output in outputs]
    output_data = to_categorical(output_data, len(label2idx))

    return input_data, output_data, idx2label

#CRIAÇÃO E TREINAMENTO DE MODELO

def create_model(input_shape, output_shape):
    model = Sequential()
    model.add(LSTM(128, input_shape=input_shape))
    model.add(Dense(output_shape, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
    return model

def train_model(model, input_data, output_data):
    model.fit(input_data, output_data, epochs=num_epochs)

def save_model(model, file_path):
    model.save(file_path)

if __name__ == "__main__":
    # Carregar e processar dados
    inputs, outputs = load_data('nlu\\train.yml')
    input_data, output_data, idx2label = process_data(inputs, outputs)

    # Criar e treinar o modelo
    model = create_model((max_seq_length, num_chars), len(idx2label))
    train_model(model, input_data, output_data)

    # Salvar o modelo treinado
    save_model(model, 'model.hdf5')


    # Criar e salvar o arquivo de rótulos
    labels_file = open('labels.txt', 'w', encoding='utf-8')
    for label in idx2label.values():
        labels_file.write(label + '\n')
    labels_file.close()