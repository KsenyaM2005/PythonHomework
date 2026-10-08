import csv

from ..check_formats import getFormat
from ..exception_decorators import exception_decorator

@exception_decorator
def write_data(file_path, data):
    if getFormat(file_path) != 'csv':
        raise ValueError("Неправильный формат: должно быть csv")

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow([key, value])