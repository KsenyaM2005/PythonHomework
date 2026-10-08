import csv
import os

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def read_data(file_path):
        data = None
        if getFormat(file_path) != 'csv':
            raise ValueError("Неправильный формат: должно быть csv")

        if os.path.isfile(file_path):
            with open(file_path) as csv_file:
                reader = csv.reader(csv_file)
                data = dict(reader)
                data = {int(i):float(key) for i,key in data.items()}
            return data
        else:
            raise ValueError("Не существует такого файла: {}".format(file_path))
