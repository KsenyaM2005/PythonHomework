import numpy as np
from ..exception_decorators import exception_decorator

@exception_decorator
def image_processing(image):
    if not isinstance(image, np.ndarray):
        image = np.array(image)

    if len(image.shape) != 2:
        raise ValueError("Неправильное кол-во размерностей изображения: {} - должно быть 2D".format(image.shape))
    num = image.shape[0] * image.shape[1]

    hist = {i:(image==i).sum() / num for i in range(0,256)}
    return hist
