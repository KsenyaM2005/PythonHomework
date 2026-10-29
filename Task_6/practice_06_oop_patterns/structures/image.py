import cv2
import numpy as np

"""
Абстрактная фабрика 
"""


from enum import Enum

class ImgType(Enum):
    BIN = 0
    MONO = 1
    COLOR = 3



class AbstractFactoryImageReader():
    def read_image(self, file_path):
        raise NotImplementedError()

class BinImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise FileNotFoundError(f"Не удалось прочитать изображение по пути: {file_path}")

        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        return binary.astype(np.uint8)

class MonochromeImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        return image

class ColorImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        return image



def get_image_reader(ident):
    if ident == 0 or ident == ImgType.BIN:
        return BinImageReader()
    elif ident == 1 or ident == ImgType.MONO:
        return MonochromeImageReader()
    elif ident == 2 or ident == ImgType.COLOR:
        return ColorImageReader()



if __name__ == "__main__":
    try:
        for i in range(3):
            print(get_image_reader(i))
    except Exception as e:
        print(e)