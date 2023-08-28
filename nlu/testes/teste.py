import pyautogui

import time

pyautogui.PAUSE = 1

# Abrir o Google Drive no computador

pyautogui.press('winleft')

pyautogui.write('brave')

pyautogui.press('enter')

time.sleep(10)

pyautogui.write('https://drive.google.com')

pyautogui.press('enter')

# Entrar na área de trabalho

pyautogui.hotkey('winleft','d')

# Clicar no arquivo e arrastar

pyautogui.moveTo(567,38)

pyautogui.mouseDown()

pyautogui.moveTo(756,635)

# Enquanto estiver arrastando mudar para a página do Google Drive

pyautogui.hotkey('alt','tab')

# Soltar o arquivo dentro do Google Drive

pyautogui.mouseUp()

# Esperar alguns segundos

time.sleep(5)