from time import sleep
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import os
import json

# Configurações
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
IMG_PATH = os.path.join(DATA_PATH, 'imgs')
BASE_URL = "https://www.shipspotting.com/photos/"
IMAGE_NUMBERS = range(3576630,3576926)
class ImageDownloader:
    """Download das imagens da lista de números fornecidos.
    """
    def __init__(self, image_numbers):
        self.image_numbers = image_numbers
        self.data = []
    def download_images(self):
        for image_number in self.image_numbers:
            image_link = f"{BASE_URL}{image_number}"
            image_name = f"{image_number}.jpg"
            image_path = os.path.join(IMG_PATH, image_name)
            Path(IMG_PATH).mkdir(parents=True, exist_ok=True)

            if os.path.exists(image_path):
                print(f"A imagem {image_name} já existe. Pulando...")
                continue

            page = requests.get(image_link)

            # Espera se o site estiver fora do ar
            while page.status_code > 500:
                sleep(10)
                print("O site está fora do ar. Tentando novamente...")
                page = requests.get(image_link)

            soup = BeautifulSoup(page.content, "html.parser")
            image_url = self._get_image_url(soup)
            category = self._get_category(soup)

            if image_url:
                self._download_image(image_url, image_path)
                print(f"Imagem {image_name} baixada com sucesso!")
                self.data.append({
                    "image_name": image_name,
                    "image_url": image_url,
                    "category": category
                })
            else:
                print(f"A imagem {image_name} não pôde ser encontrada.")

        self._save_data()

    def _get_image_url(self, soup):
        """Obtém a URL da imagem com base na estrutura da página.
        """
        image_element = soup.find("meta", attrs={"property": "og:image"})
        if image_element:
            return image_element["content"]
        return None

    def _get_category(self, soup):
        """Obtém a categoria com base na estrutura da página.
        """
        category_element = soup.find("a", href="/photos/gallery?category=10")
        if category_element:
            return category_element.text.strip()
        return None

    def _download_image(self, image_url, image_path):
        """Faz o download da imagem com base na URL fornecida.
        """
        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)

    def _save_data(self):
        """Salva os dados em um arquivo JSON.
        """
        json_data = json.dumps(self.data, indent=4)
        json_path = os.path.join(DATA_PATH, 'data.json')
        with open(json_path, 'w') as file:
            file.write(json_data)

if __name__ == '__main__':
    downloader = ImageDownloader(IMAGE_NUMBERS)
    downloader.download_images()
'''
'''
import os

folder_path = "data/imgs9"  # Caminho para a pasta de imagens
image_numbers = []  # Vetor para armazenar os números das imagens

# Verifica se a pasta existe
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Percorre todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        # Verifica se é um arquivo de imagem
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Extrai o número do nome do arquivo
            image_number = os.path.splitext(filename)[0]
            # Converte o número para inteiro e adiciona ao vetor
            image_numbers.append(int(image_number))
else:
    print(f"A pasta '{folder_path}' não existe.")

# Imprime o vetor com os números das imagens
print("Vetor com os números das imagens:")
print(image_numbers)
