import cv2 as cv
import numpy as np
from ..processor import histogram


def processing(src):
    if src is None:
        raise ValueError("Неправильный источник изображения!")

    image = np.array(src).astype(np.uint8)

    hist = np.array(list(histogram.image_processing(image).values()))
    cdf = np.array([np.sum(hist[:k+1]) for k in range(len(hist))])

    cdf_min = cdf[cdf > 0].min()  # первое ненулевое
    N = hist.sum()
    lut = np.round((cdf - cdf_min) / (N - cdf_min) * 255).astype(np.uint8)
    lut = np.clip(lut, 0, 255)

    return lut[image]
