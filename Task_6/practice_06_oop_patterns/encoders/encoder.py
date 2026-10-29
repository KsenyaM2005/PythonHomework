import sys
import struct
import csv
import json
import cv2
import numpy as np


class HistEncoder:
    @staticmethod
    def encode(data, file_path):
        raise NotImplementedError()


class BinHistEncoder(HistEncoder):
    @staticmethod
    def encode(data, file_path):
        values = [data.get(i, 0.0) for i in range(256)]

        with open(file_path, 'wb') as file:
            packed = struct.pack('f' * 256, *values)
            file.write(packed)


class CsvHistEncoder(HistEncoder):
    @staticmethod
    def encode(data, file_path):
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in data.items():
                writer.writerow([key, value])


class TxtHistEncoder(HistEncoder):
    @staticmethod
    def encode(data, file_path):
        with open(file_path, 'w') as file:
            # Формат: ключ значение (каждая пара на новой строке)
            items = []
            for key, value in sorted(data.items()):
                items.append(str(key) + " " + f"{value:.6f}")
            file.write("\n".join(items))


class JsonHistEncoder(HistEncoder):
    @staticmethod
    def encode(data, file_path):
        keys = list(data.keys())
        values = list(data.values())
        payload = {
            "keys": keys,
            "values": values
        }
        with open(file_path, 'w') as file:
            json.dump(payload, file)


class ImageHistEncoder(HistEncoder):
    @staticmethod
    def encode(data, file_path, height=256, width=256):
        max_val = max(data.values()) if data else 1.0
        if max_val == 0:
            max_val = 1.0  # защита от деления на ноль

        # Создаем пустое изображение (grayscale)
        img = np.zeros((height, width), dtype=np.uint8)

        for bin_idx, value in data.items():
            if 0 <= bin_idx < width:
                # Нормализуем высоту столбца
                h = int((value / max_val) * height)
                # Заполняем столбец сверху вниз
                img[height - h:, bin_idx] = int((value / max_val) * 255)

        cv2.imwrite(file_path, img)


