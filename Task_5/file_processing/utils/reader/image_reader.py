import cv2
import os

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def read_data(file_path):
    if getFormat(file_path) != 'img':
        raise ValueError("Неправильный формат: должен быть один из допустимых форматов изображений")

    if os.path.isfile(file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    else:
        raise ValueError("Не существует такого файла: {}".format(file_path))
    return image