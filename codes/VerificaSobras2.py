import os

imgs_folder = "data/imgs"  # Pasta das imagens
meta_folder = "data/meta"  # Pasta dos metadados
missing_jsons = []  # Imagens sem arquivo .json correspondente
missing_images = []  # Arquivos .json sem imagem correspondente

# Verifica se as pastas existem
if os.path.exists(imgs_folder) and os.path.isdir(imgs_folder) and \
   os.path.exists(meta_folder) and os.path.isdir(meta_folder):

    # Percorre as imagens na pasta "imgs"
    for img_file in os.listdir(imgs_folder):
        img_name = os.path.splitext(img_file)[0]
        json_file = os.path.join(meta_folder, f"{img_name}.json")

        # Verifica se o arquivo .json existe
        if not os.path.exists(json_file):
            missing_jsons.append(img_file)

    # Percorre os arquivos .json na pasta "meta"
    for json_file in os.listdir(meta_folder):
        json_name = os.path.splitext(json_file)[0]
        img_file = os.path.join(imgs_folder, f"{json_name}.jpg")

        # Verifica se a imagem correspondente existe
        if not os.path.exists(img_file):
            missing_images.append(json_file)

    # Imprime as imagens sem arquivo .json correspondente
    print("Imagens sem arquivo .json correspondente:")
    print(missing_jsons)

    # Imprime os arquivos .json sem imagem correspondente
    print("Arquivos .json sem imagem correspondente:")
    print(missing_images)

else:
    print("As pastas 'imgs' e/ou 'meta' não existem.")