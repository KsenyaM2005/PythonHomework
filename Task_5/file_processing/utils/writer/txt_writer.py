from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def write_data(file_path, data):
    if getFormat(file_path) != 'txt':
        raise ValueError("Неправильный формат: должно быть json")

    with open(file_path, "w") as file:
        for key, value in data.items():
            file.write('{} {} \n'.format(key,value))
