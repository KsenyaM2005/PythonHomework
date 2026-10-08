import os

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def read_data(file_path):
    if getFormat(file_path) != 'txt':
        raise ValueError("Неправильный формат: должно быть txt")

    data = None

    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            source = file.read().split()
            data = { int(i): float(source[2*i+1]) for i in range(len(source) // 2)}
    else:
        raise ValueError("Не существует такого файла: {}".format(file_path))

    return data