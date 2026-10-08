import numpy as np
import cv2

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def write_data(file_path, data):
    if getFormat(file_path) != 'img':
        raise ValueError("Неправильный формат: должен быть один из допустимых форматов изображений")

    cv2.imwrite(file_path, data)