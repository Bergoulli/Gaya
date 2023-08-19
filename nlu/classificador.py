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

# if __name__ == "__main__":
#     # Carregar o modelo treinado
#     model = load_model('model.hdf5')
    
#     # Carregar rótulos
#     labels = load_labels('labels.txt')

#     # Classificação de texto em uma entidade
#     while True:
#         text = input('Digite algo: ')
#         classify(model, labels, text)
