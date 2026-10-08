import sys
import struct
import os

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def read_data(file_path):
    if getFormat(file_path) != 'bin':
        raise ValueError("Неправильный формат: должно быть bin")

    data = []
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            data = struct.unpack('f'*256, file.read(sys.getsizeof(0.0)*256))
    else:
        raise ValueError("Не существует такого файла: {}".format(file_path))

    data ={i: data[i] for i in range(len(data))}

    return data