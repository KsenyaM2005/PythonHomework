from abc import ABC, abstractmethod
import numpy as np


class Image(ABC):
    def __init__(self, pixels):
        self._pixels = None
        self.pixels = pixels


    @property
    @abstractmethod
    def pixels(self):
        ...

    @pixels.setter
    @abstractmethod
    def pixels(self, value):
        ...

    @staticmethod
    @abstractmethod
    def _validate(pixels) -> np.ndarray:
        ...


    @property
    def shape(self):
        return self._pixels.shape





class BinaryImage(Image):
    @staticmethod
    def _validate(pixels) -> np.ndarray:
        arr = _as_ndarray(pixels)
        if arr.ndim != 2:
            raise ValueError(
                "BinaryImage: ожидается 2D-матрица, получено {}D".format(arr.ndim)
            )
        if not np.all(np.isin(arr, (0, 1))):
            raise ValueError(
                "BinaryImage: допустимы только значения 0 и 1"
            )
        return arr.astype(np.uint8)

    @property
    def pixels(self):
        return self._pixels

    @pixels.setter
    def pixels(self, value):
        self._pixels = self._validate(value)




class MonochromImage(Image):
    @staticmethod
    def _validate(pixels) -> np.ndarray:
        arr = _as_ndarray(pixels)
        if arr.ndim != 2:
            raise ValueError(
                "MonochromImage: ожидается 2D-матрица, получено {}D".format(arr.ndim)
            )
        if not np.issubdtype(arr.dtype, np.number):
            raise ValueError(
                "MonochromImage: матрица должна содержать числа"
            )
        return arr

    @property
    def pixels(self):
        return self._pixels

    @pixels.setter
    def pixels(self, value):
        self._pixels = self._validate(value)




class ColorImage(Image):
    @staticmethod
    def _validate(pixels) -> np.ndarray:
        arr = _as_ndarray(pixels)

        if isinstance(pixels, (list, tuple)) and len(pixels) == 3:
            channels = [_as_ndarray(ch) for ch in pixels]
            for ch in channels:
                if ch.ndim != 2:
                    raise ValueError(
                        "ColorImage: каждый канал должен быть 2D-матрицей"
                    )
            if not (channels[0].shape == channels[1].shape == channels[2].shape):
                raise ValueError(
                    "ColorImage: все три канала должны иметь одинаковую форму"
                )
            return np.stack(channels, axis=-1)

        raise ValueError(
            "ColorImage: ожидается последовательность из трёх 2D-матриц"
        )

    @property
    def pixels(self):
        return self._pixels

    @pixels.setter
    def pixels(self, value):
        self._pixels = self._validate(value)


    @property
    def red(self):
        return self._pixels[:, :, 0]

    @property
    def green(self):
        return self._pixels[:, :, 1]

    @property
    def blue(self):
        return self._pixels[:, :, 2]





def _as_ndarray(pixels) -> np.ndarray:
    if isinstance(pixels, np.ndarray):
        return pixels
    if isinstance(pixels, (list, tuple)):
        try:
            return np.asarray(pixels)
        except Exception as e:
            raise ValueError("Не удалось преобразовать данные в ndarray: {}".format(e))
    raise ValueError(
        "Ожидается np.ndarray или последовательность, получено {}".format(type(pixels))
    )