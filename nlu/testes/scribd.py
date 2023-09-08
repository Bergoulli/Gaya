import bs4 as bs
from selenium import webdriver
import os
import re
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)

url = 'https://www.scribd.com/document/284732331/Text-Monochrome-Colour-Television-R-R-Gulati-pdf'
browser.get(url)
source = browser.page_source

soup = bs.BeautifulSoup(source, "lxml")
images = []

for element in soup.find_all('div', attrs={'class': "ie_fix"}):
    try:
        images.append(element.find('img').get('src'))
    except:
        pass

path = os.path.dirname(os.path.abspath(__file__))
name = url.split('/')[-1].split('-')[0]
newpath = os.path.join(path, name)

if not os.path.exists(newpath):
    os.mkdir(newpath)

for index, image_url in enumerate(images, start=1):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(os.path.join(newpath, f'page_{index}.jpg'), 'JPEG')

image_files = [os.path.join(newpath, f'page_{index}.jpg') for index in range(1, len(images) + 1)]

if image_files:
    pdf_path = os.path.join(newpath, 'output.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)

    for image_file in image_files:
        c.drawImage(image_file, 0, 0, width=letter[0], height=letter[1])
        c.showPage()

    c.save()

    print(f"PDF criado em: {pdf_path}")
else:
    print("Nenhuma imagem encontrada para criar o PDF.")

browser.quit()
