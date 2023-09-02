import tkinter as tk
from PIL import Image, ImageTk

def imagem():

    # Lista de caminhos das imagens
    image_paths = ["sprite_0.png", "sprite_1.png", "sprite_2.png", "sprite_3.png",]


    # Variável global para a imagem atual
    current_image = None

    # Função para alternar as imagens
    def alternar_imagem(index=0):
        global current_image
        
        if index >= len(image_paths):
            index = 0
        image = Image.open(image_paths[index])
        photo = ImageTk.PhotoImage(image=image)
        label.config(image=photo)
        current_image = photo
        
        root.after(2000, alternar_imagem, index + 1)  # Muda a imagem a cada 2000ms (2 segundos)

    # Crie a janela principal
    root = tk.Tk()
    root.title("Exibição de Imagens Rotativas")

    # Crie um rótulo para exibir as imagens
    label = tk.Label(root)
    label.pack()

    # Inicie o ciclo de alternância das imagens
    alternar_imagem()

    root.mainloop()


