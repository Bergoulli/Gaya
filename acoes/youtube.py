from pytube import YouTube
import pyperclip
import time
import pyautogui
import os
import shutil
from moviepy.editor import AudioFileClip
import io

def musica_download():
    time.sleep(5)
    pyautogui.click(310, 57, clicks=1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    link_copiado = pyperclip.paste()
    
    if link_copiado.split('//')[0] == 'https:':
        try:
            video = YouTube(link_copiado)
            
            # Obtém o título do vídeo
            video_title = video.title
            
            # Obtenha a stream de melhor qualidade que inclui áudio
            audio_stream = video.streams.filter(only_audio=True).first()
            
            if audio_stream:
                # Baixa o áudio como um arquivo temporário
                temp_audio_filename = 'temp_audio.mp4'
                audio_stream.download(filename=temp_audio_filename)
                
                # Converte o áudio para MP3
                temp_audio_path = os.path.join('', temp_audio_filename)
                audio = AudioFileClip(temp_audio_path)
                
                audio_filename = f'{video_title}.mp3'
                destination_folder = "musicas"
                
                if not os.path.exists(destination_folder):
                    os.mkdir(destination_folder)
                
                destination_path = os.path.join(destination_folder, audio_filename)
                audio.write_audiofile(destination_path, codec='mp3')
                
                # Remove os arquivos temporários
                os.remove(temp_audio_path)
                
                return video
            else:
                print("Não foi possível encontrar a stream de áudio adequada.")
        except Exception as e:
            print("Erro durante o download ou conversão do áudio:", str(e))
    else:
        print("URL inválida")

def video_download():
    pyautogui.click(310, 57, clicks=1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    link_copiado = pyperclip.paste()
    
    if link_copiado.split('//')[0] == 'https:':
        try:
            video = YouTube(link_copiado)
            
            # Obtém o título do vídeo
            video_title = video.title
            
            # Obtenha a stream de melhor qualidade que inclui vídeo e áudio no formato MP4
            video_stream = video.streams.filter(file_extension='mp4').get_highest_resolution()
            
            if video_stream:
                # Baixa o vídeo com áudio
                video_stream.download()
                
                # Obtém o nome do arquivo original
                original_filename = video_stream.default_filename
                
                # Move o arquivo para a pasta "videos"
                destination_folder = "videos"
                if not os.path.exists(destination_folder):
                    os.mkdir(destination_folder)
                
                destination_path = os.path.join(destination_folder, f'{video_title}.mp4')
                shutil.move(original_filename, destination_path)
                
                return video
            else:
                print("Não foi possível encontrar a stream de vídeo com áudio em formato MP4 adequada.")
        except Exception as e:
            print("Erro durante o download:", str(e))
    else:
        print("URL inválida")
