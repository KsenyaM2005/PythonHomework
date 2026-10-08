from image_processing.image import ColorImage, MonochromImage, BinaryImage
import numpy as np
import math


class Converter:

    @staticmethod
    def mono_to_mono(img: MonochromImage,
                     hist: dict = None) -> MonochromImage:
        arr = img.pixels.astype(np.float64)

        if hist is None:
            hist = Converter._histogram(arr)

        corrected = Converter.stat_correction(hist, arr)
        return MonochromImage(corrected)


    @staticmethod
    def color_to_color(img: ColorImage,
                       hists: list = None) -> ColorImage:
        arr = img.pixels.astype(np.float64)

        if hists is None:
            hists = [Converter._histogram(arr[:, :, c]) for c in range(3)]

        channels = []
        for c in range(3):
            ch = arr[:, :, c]
            channels.append(Converter.stat_correction(hists[c], ch))

        return ColorImage(channels)



    @staticmethod
    def binary_to_binary(img: BinaryImage) -> BinaryImage:
        return BinaryImage(img.pixels.copy())



    @staticmethod
    def color_to_mono(img: ColorImage) -> MonochromImage:
        arr = img.pixels.astype(np.float64)
        gray = arr.mean(axis=2)
        return MonochromImage(gray)



    @staticmethod
    def mono_to_color(img: MonochromImage,
                      palette: dict) -> ColorImage:
        if not palette:
            raise ValueError("Палитра пуста")

        keys = np.array(sorted(palette.keys()), dtype=np.float64)
        colors = np.array([palette[k] for k in sorted(palette.keys())],
                          dtype=np.float64)

        arr = img.pixels.astype(np.float64)
        h, w = arr.shape
        result = np.empty((h, w, 3), dtype=np.float64)

        flat = arr.ravel()
        idx = np.abs(flat[:, None] - keys[None, :]).argmin(axis=1)
        result = colors[idx].reshape(h, w, 3)

        return ColorImage([result[:, :, 0],
                           result[:, :, 1],
                           result[:, :, 2]])


    @staticmethod
    def mono_to_binary(img: MonochromImage,
                       threshold: float = None) -> BinaryImage:

        arr = img.pixels.astype(np.float64)

        binary = (arr > threshold).astype(np.uint8)
        return BinaryImage(binary)



    @staticmethod
    def binary_to_mono(img: BinaryImage) -> MonochromImage:
        arr = img.pixels.astype(bool)
        h, w = arr.shape

        # «белые» — True.
        # нет белых — вся карта 0
        ys, xs = np.nonzero(arr)
        if len(ys) == 0:
            return MonochromImage(np.zeros((h, w), dtype=np.float64))

        yy, xx = np.mgrid[0:h, 0:w]
        dist = np.full((h, w), np.inf)

        for y0, x0 in zip(ys, xs):
            d = np.sqrt((yy - y0) ** 2 + (xx - x0) ** 2)
            dist = np.minimum(dist, d)

        mx = dist.max()
        if mx > 0:
            dist = dist / mx * 255.0
        return MonochromImage(dist)



    @staticmethod
    def color_to_binary(img: ColorImage,
                        threshold: float = None) -> BinaryImage:
        mono = Converter.color_to_mono(img)
        return Converter.mono_to_binary(mono, threshold)



    @staticmethod
    def binary_to_color(img: BinaryImage,
                        palette: dict) -> ColorImage:
        mono = Converter.binary_to_mono(img)
        return Converter.mono_to_color(mono, palette)


    # Старые функции для гистограммы, коррекции

    @staticmethod
    def _histogram(image: np.ndarray):
        num = image.shape[0] * image.shape[1]

        hist = {i: (image == i).sum() / num for i in range(0, 256)}
        return hist

    @staticmethod
    def stat_correction(hist: dict, image: np.ndarray):
        av1 = np.array([key * value for key, value in hist.items()]).sum()
        std1 = math.sqrt(np.array([value * (key - av1) ** 2 for key, value in hist.items()]).sum())

        av2 = image.mean()
        std2 = image.std()

        if std2 == 0:
            return np.full_like(image, av1, dtype=np.float64)

        image = std1 * (image - av2) / std2 + av1

        return image