import cv2 as cv
import numpy as np

def processing(image):
    if image is None:
        raise ValueError("Неправильный источник изображения!")

    gamma = 1.0

    try:
        gamma = float(input('* Enter the gamma: '))
    except ValueError:
        print('Error, not a number')

    img = image.astype(np.float32) / 255.0
    out = np.power(img, gamma) * 255.0
    return np.clip(out, 0, 255).astype(np.uint8)

