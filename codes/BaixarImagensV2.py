'''
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
IMAGE_NUMBERS = [42, 17]  # Números das imagens a serem baixadas

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
from time import sleep
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import os
import json

# Configurações
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
IMG_PATH = os.path.join(DATA_PATH, 'imgs')
META_PATH = os.path.join(DATA_PATH, 'meta')
BASE_URL = "https://www.shipspotting.com/photos/"
IMAGE_NUMBERS = [42, 17, 1]  # Números das imagens a serem baixadas

class ImageDownloader:
    """Download das imagens da lista de números fornecidos.
    """
    def __init__(self, image_numbers):
        self.image_numbers = image_numbers

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
                metadata = self._get_metadata(soup)
                self._save_metadata(image_number, metadata)
            else:
                print(f"A imagem {image_name} não pôde ser encontrada.")

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

    def _get_metadata(self, soup):
        """Obtém os metadados da imagem com base na estrutura da página.
        """
        metadata = {
            "Photographer:": "",
            "Captured:": "",
            "Title:": "",
            "Location:": "",
            "Photo Category:": "",
            "Added:": "",
            "Hits:": "",
            "Total hits:": "",
            "Current flag:": "",
            "Home port:": "",
            "Current name:": "",
            "Vessel Type:": "",
            "Class society:": "",
            "Callsign:": "",
            "IMO:": "",
            "MMSI:": "",
            "Build year:": "",
            "Photos:": "",
            "Gross tonnage:": "",
            "Summer DWT:": "",
            "Length:": "",
            "Beam:": "",
            "Draught:": "",
            "Categories": []
        }

        items = soup.find_all("div", class_="summary-photo__card-general__label")
        for item in items:
            span_items = item.find_all("span")

            if len(span_items) < 2:
                continue

            key = span_items[0].text.strip()
            value = span_items[1].text.strip()
            metadata[key] = value

        categories = soup.find_all("p", class_="card-categories__container__value")
        for category in categories:
            span_items = category.find_all("span")

            if len(span_items) > 0:
                metadata["Categories"].append(span_items[0].text.strip())

        return metadata

    def _save_metadata(self, image_number, metadata):
        """Salva os metadados em um arquivo JSON.
        """
        json_data = json.dumps(metadata, indent=4)
        json_path = os.path.join(META_PATH, f"{image_number}.json")
        with open(json_path, 'w') as file:
            file.write(json_data)

if __name__ == '__main__':
    downloader = ImageDownloader(IMAGE_NUMBERS)
    downloader.download_images()
'''
'''
from time import sleep
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import os
import json
import threading

# Configurações
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
IMG_PATH = os.path.join(DATA_PATH, 'imgs')
META_PATH = os.path.join(DATA_PATH, 'meta')
BASE_URL = "https://www.shipspotting.com/photos/"
IMAGE_NUMBERS = range(1,121)  # Números das imagens a serem baixadas
NUM_THREADS = 4  # Número de threads para download paralelo

class ImageDownloader:
    """Download das imagens da lista de números fornecidos.
    """
    def __init__(self, image_numbers):
        self.image_numbers = image_numbers
        self.lock = threading.Lock()

    def download_images(self):
        threads = []

        for i in range(0, len(self.image_numbers), NUM_THREADS):
            image_numbers_subset = self.image_numbers[i:i+NUM_THREADS]

            for image_number in image_numbers_subset:
                thread = threading.Thread(target=self._download_image, args=(image_number,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

    def _download_image(self, image_number):
        image_link = f"{BASE_URL}{image_number}"
        image_name = f"{image_number}.jpg"
        image_path = os.path.join(IMG_PATH, image_name)
        Path(IMG_PATH).mkdir(parents=True, exist_ok=True)

        if os.path.exists(image_path):
            print(f"A imagem {image_name} já existe. Pulando...")
            return

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
            self._download_image_file(image_url, image_path)
            print(f"Imagem {image_name} baixada com sucesso!")
            metadata = self._get_metadata(soup)
            self._save_metadata(image_number, metadata)
        else:
            print(f"A imagem {image_name} não pôde ser encontrada.")

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

    def _download_image_file(self, image_url, image_path):
        """Faz o download da imagem com base na URL fornecida.
        """
        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)

    def _get_metadata(self, soup):
        """Obtém os metadados da imagem com base na estrutura da página.
        """
        metadata = {
            "Photographer:": "",
            "Captured:": "",
            "Title:": "",
            "Location:": "",
            "Photo Category:": "",
            "Added:": "",
            "Hits:": "",
            "Total hits:": "",
            "Current flag:": "",
            "Home port:": "",
            "Current name:": "",
            "Vessel Type:": "",
            "Class society:": "",
            "Callsign:": "",
            "IMO:": "",
            "MMSI:": "",
            "Build year:": "",
            "Photos:": "",
            "Gross tonnage:": "",
            "Summer DWT:": "",
            "Length:": "",
            "Beam:": "",
            "Draught:": "",
            "Categories": []
        }

        items = soup.find_all("div", class_="summary-photo__card-general__label")
        for item in items:
            span_items = item.find_all("span")

            if len(span_items) < 2:
                continue

            key = span_items[0].text.strip()
            value = span_items[1].text.strip()
            metadata[key] = value

        categories = soup.find_all("p", class_="card-categories__container__value")
        for category in categories:
            span_items = category.find_all("span")

            if len(span_items) > 0:
                metadata["Categories"].append(span_items[0].text.strip())

        return metadata

    def _save_metadata(self, image_number, metadata):
        """Salva os metadados em um arquivo JSON.
        """
        json_data = json.dumps(metadata, indent=4)
        json_path = os.path.join(META_PATH, f"{image_number}.json")
        with self.lock:
            with open(json_path, 'w') as file:
                file.write(json_data)

if __name__ == '__main__':
    downloader = ImageDownloader(IMAGE_NUMBERS)
    downloader.download_images()
'''


from time import sleep
from bs4 import BeautifulSoup
import requests
import os
import json
import threading
import shutil

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
RESTONAVIO_PATH = os.path.join(DATA_PATH, 'restonavio2')
BASE_URL = "https://www.shipspotting.com/photos/"
NUM_THREADS = 16  # Número de threads para download paralelo
DOWNLOAD_BATCH_SIZE = 5000  # Tamanho do lote para sinal de vida

class ImageDownloader:
    def __init__(self):
        self.lock = threading.Lock()

    def download_images(self):
        existing_images = self.get_existing_images()
        total_images = len(existing_images)
        print(f"Total de imagens existentes: {total_images}")
        print("Números das imagens existentes:")
        for image_number in existing_images:
            print(image_number)

        threads = []
        for i in range(0, total_images, NUM_THREADS):
            image_numbers_subset = list(existing_images)[i:i + NUM_THREADS]

            for image_number in image_numbers_subset:
                thread = threading.Thread(target=self._download_image, args=(image_number,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            if i % DOWNLOAD_BATCH_SIZE == 0:
                print(f"Sinal de vida: Baixados {i} de {total_images} metadados.")

    def get_existing_images(self):
        existing_images = set()

        for filename in os.listdir(RESTONAVIO_PATH):
            if filename.endswith(".jpg"):
                image_number = int(os.path.splitext(filename)[0])
                existing_images.add(image_number)

        return existing_images

    def _download_image(self, image_number):
        image_link = f"{BASE_URL}{image_number}"
        image_name = f"{image_number}.jpg"
        json_path = os.path.join(RESTONAVIO_PATH, f"{image_number}.json")

        if os.path.exists(json_path):
            print(f"O arquivo JSON para a imagem {image_name} já existe. Pulando...")
            return

        page = requests.get(image_link)

        while page.status_code > 500:
            sleep(100)
            print("O site está fora do ar. Tentando novamente...")
            page = requests.get(image_link)

        soup = BeautifulSoup(page.content, "html.parser")
        metadata = self._get_metadata(soup)

        if metadata:
            self._save_metadata(image_number, metadata)
            print(f"Metadados da imagem {image_name} salvos com sucesso!")

    def _get_metadata(self, soup):
        metadata = {}

        items = soup.find_all("div", class_="summary-photo__card-general__label")
        for item in items:
            span_items = item.find_all("span")

            if len(span_items) < 2:
                continue

            key = span_items[0].text.strip().rstrip(":")
            value = span_items[1].text.strip()
            metadata[key] = value

        categories = soup.find_all("p", class_="card-categories__container__value")
        metadata["Categories"] = [span.text.strip() for category in categories for span in category.find_all("span")]

        return metadata

    def _save_metadata(self, image_number, metadata):
        json_data = json.dumps(metadata, indent=4)
        json_path = os.path.join(RESTONAVIO_PATH, f"{image_number}.json")
        with self.lock:
            with open(json_path, 'w') as file:
                file.write(json_data)

if __name__ == '__main__':
    downloader = ImageDownloader()
    downloader.download_images()






'''

from time import sleep
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import os
import json
import threading

# Configurações
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
IMG_PATH = os.path.join(DATA_PATH, 'imgs')
META_PATH = os.path.join(DATA_PATH, 'meta')
BASE_URL = "https://www.shipspotting.com/photos/"
MIN_IMAGE_NUMBER = 2566630  # Número mínimo da imagem
MAX_IMAGE_NUMBER = 3566630  # Número máximo da imagem
NUM_THREADS = 16  # Número de threads para download paralelo

class ImageDownloader:
    """Download das imagens da lista de números fornecidos.
    """
    def __init__(self, min_image_number, max_image_number):
        self.min_image_number = min_image_number
        self.max_image_number = max_image_number
        self.lock = threading.Lock()

    def download_images(self):
        missing_images = self.get_missing_images()
        print(f"Total de imagens faltando: {len(missing_images)}")
        print("Números das imagens faltantes:")
        for image_number in missing_images:
            print(image_number)

        threads = []
        total_threads = min(NUM_THREADS, len(missing_images))  # Garante que o número de threads não exceda o número de imagens faltantes
        chunk_size = len(missing_images) // total_threads  # Calcula o tamanho de cada chunk para cada thread
        for i in range(total_threads):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i != total_threads - 1 else len(missing_images)
            image_numbers_subset = missing_images[start_index:end_index]

            for image_number in image_numbers_subset:
                thread = threading.Thread(target=self._download_image, args=(image_number,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

    def get_missing_images(self):
        """Verifica quais imagens estão faltando na pasta de imagens.
        """
        missing_images = []
        existing_images = set()

        for filename in os.listdir(IMG_PATH):
            if filename.endswith(".jpg"):
                image_number = int(os.path.splitext(filename)[0])
                existing_images.add(image_number)

        for image_number in range(self.min_image_number, self.max_image_number + 1):
            if image_number not in existing_images:
                missing_images.append(image_number)

        return missing_images

    def _download_image(self, image_number):
        image_link = f"{BASE_URL}{image_number}"
        image_name = f"{image_number}.jpg"
        image_path = os.path.join(IMG_PATH, image_name)
        Path(IMG_PATH).mkdir(parents=True, exist_ok=True)

        if os.path.exists(image_path):
            print(f"A imagem {image_name} já existe. Pulando...")
            return

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
            self._download_image_file(image_url, image_path)
            print(f"Imagem {image_name} baixada com sucesso!")
            metadata = self._get_metadata(soup)
            self._save_metadata(image_number, metadata)
        else:
            print(f"A imagem {image_name} não pôde ser encontrada.")

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

    def _download_image_file(self, image_url, image_path):
        """Faz o download da imagem com base na URL fornecida.
        """
        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)

    def _get_metadata(self, soup):
        """Obtém os metadados da imagem com base na estrutura da página.
        """
        metadata = {
            "Photographer:": "",
            "Captured:": "",
            "Title:": "",
            "Location:": "",
            "Photo Category:": "",
            "Added:": "",
            "Hits:": "",
            "Total hits:": "",
            "Current flag:": "",
            "Home port:": "",
            "Current name:": "",
            "Vessel Type:": "",
            "Class society:": "",
            "Callsign:": "",
            "IMO:": "",
            "MMSI:": "",
            "Build year:": "",
            "Photos:": "",
            "Gross tonnage:": "",
            "Summer DWT:": "",
            "Length:": "",
            "Beam:": "",
            "Draught:": "",
            "Categories": []
        }

        items = soup.find_all("div", class_="summary-photo__card-general__label")
        for item in items:
            span_items = item.find_all("span")

            if len(span_items) < 2:
                continue

            key = span_items[0].text.strip()
            value = span_items[1].text.strip()
            metadata[key] = value

        categories = soup.find_all("p", class_="card-categories__container__value")
        for category in categories:
            span_items = category.find_all("span")

            if len(span_items) > 0:
                metadata["Categories"].append(span_items[0].text.strip())

        return metadata

    def _save_metadata(self, image_number, metadata):
        """Salva os metadados em um arquivo JSON.
        """
        json_data = json.dumps(metadata, indent=4)
        json_path = os.path.join(META_PATH, f"{image_number}.json")
        with self.lock:
            with open(json_path, 'w') as file:
                file.write(json_data)

if __name__ == '__main__':
    downloader = ImageDownloader(MIN_IMAGE_NUMBER, MAX_IMAGE_NUMBER)
    downloader.download_images()'''

