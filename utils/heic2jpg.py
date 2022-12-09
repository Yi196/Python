import os

import whatimage
import pyheif
from PIL import Image
import glob


def heic_to_jpg(heic_img_path):
    with open(heic_img_path, 'rb') as f:
        heic_img = f.read()

    img_format = whatimage.identify_image(heic_img)
    # print('img_format = ', img_format)
    if img_format in ['heic']:
        img = pyheif.read_heif(heic_img)
        # print('img = ', img)
        # print('img.metadata = ', img.metadata)
        pi = Image.frombytes(mode=img.mode, size=img.size, data=img.data)
        # print('pi = ', pi)
        pi.save(heic_img_path[:-5] + ".jpg", format="jpeg")


if __name__ == "__main__":
    file_paths = r'/home/mafneg/桌面/第二批转格式/'

    for parent_dir, child_dir, file_name in os.walk(file_paths):
        if not file_name:
            continue
        for name in file_name:
            img_path = os.path.join(parent_dir, name)
            print(img_path)
            if not img_path.endswith('.HEIC'):
                continue
            heic_to_jpg(img_path)
