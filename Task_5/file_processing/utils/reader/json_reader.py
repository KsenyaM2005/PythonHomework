import json
import os

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def read_data(file_path):
    if getFormat(file_path) != 'json':
        raise ValueError("Неправильный формат: должно быть json")
    data = None

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        raise ValueError("Не существует такого файла: {}".format(file_path))

    data = {data['keys'][i]:data['values'][i] for i in range(len(data['keys']))}

    return data
