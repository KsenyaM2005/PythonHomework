import math
import numpy as np
from ..exception_decorators import exception_decorator

@exception_decorator
def processing(hist, image):
    av1 = np.array([key*value for key, value in hist.items()]).sum()
    std1 = math.sqrt(np.array([ value * (key - av1)**2 for key, value in hist.items()]).sum())

    av2 = image.mean()
    std2 = image.std()

    if std2 == 0:
        return np.full_like(image, av1, dtype=np.float64)

    image = std1 * (image - av2) / std2 + av1

    return image