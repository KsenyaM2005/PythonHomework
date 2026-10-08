import json

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def write_data(file_path, data):
    if getFormat(file_path) != 'json':
        raise ValueError("Неправильный формат: должно быть json")

    reform_data = {'keys':list(data.keys()),
                   'values':list(data.values())}

    with open(file_path, 'w') as file:
        json.dump(reform_data, file)