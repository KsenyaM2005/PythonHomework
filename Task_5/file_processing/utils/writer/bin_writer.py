import struct

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def write_data(file_path, data):
    if getFormat(file_path) != 'bin':
        raise ValueError("Неправильный формат: должно быть bin")

    with open(file_path, "wb") as file:
        binary_data = b''.join(struct.pack('f', f) for f in list(data.values()))
        file.write(binary_data)