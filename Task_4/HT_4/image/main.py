import numpy as np

from image_processing.image import BinaryImage, ColorImage, MonochromImage
from image_processing.converter import Converter


def converter_test() -> None:
    print("=== converter_test ===")

    #  Цветное → Монохром
    color = ColorImage([
        np.array([[0, 255], [0, 255]], dtype=np.uint8),   # R
        np.array([[0, 255], [0, 255]], dtype=np.uint8),   # G
        np.array([[0, 0],   [255, 255]], dtype=np.uint8), # B
    ])
    mono = Converter.color_to_mono(color)
    print("color_to_mono:\n", mono.pixels)
    expected = np.array([[0, 170], [85, 255]], dtype=float)
    assert np.allclose(mono.pixels, expected), mono.pixels

    # Монохром → Бинарное
    mono_test = MonochromImage(np.array([[10, 100, 200],
                                         [50, 150, 250]], dtype=np.uint8))
    binary_manual = Converter.mono_to_binary(mono_test, threshold=128)
    print("mono_to_binary (thr=128):\n", binary_manual.pixels)
    assert binary_manual.pixels.dtype == np.uint8
    assert np.array_equal(
        binary_manual.pixels,
        np.array([[0, 0, 1], [0, 1, 1]], dtype=np.uint8)
    )


    #  Бинарное → Бинарное
    b_in = BinaryImage(np.array([[0, 1], [1, 0]], dtype=np.uint8))
    b_out = Converter.binary_to_binary(b_in)
    assert np.array_equal(b_in.pixels, b_out.pixels)
    assert b_in is not b_out
    print("binary_to_binary OK")


    #  Бинарное → Монохром
    b = BinaryImage(np.array([[0, 0, 0],
                              [0, 1, 0],
                              [0, 0, 0]], dtype=np.uint8))
    dist = Converter.binary_to_mono(b)
    print("binary_to_mono (distance):\n", dist.pixels)
    assert dist.pixels[1, 1] == 0.0
    assert np.isclose(dist.pixels.max(), 255.0)

    # нет белых пикселей → нулевая карта
    empty = BinaryImage(np.zeros((3, 3), dtype=np.uint8))
    dist_empty = Converter.binary_to_mono(empty)
    assert np.all(dist_empty.pixels == 0)

    #  Монохром → Цветное: палитра
    mono_gray = MonochromImage(np.array([[0, 128],
                                         [200, 255]], dtype=np.uint8))
    palette = {0: (0, 0, 0), 128: (128, 0, 0), 255: (255, 255, 255)}
    recolored = Converter.mono_to_color(mono_gray, palette)
    print("mono_to_color:\n", recolored.pixels)
    assert recolored.shape == (2, 2, 3)
    # 0 → чёрный, 255 → белый, 128 → красный, 200 → ближайший из {128, 255} = 255
    assert np.array_equal(recolored.pixels[0, 0], (0, 0, 0))
    assert np.array_equal(recolored.pixels[0, 1], (128, 0, 0))
    assert np.array_equal(recolored.pixels[1, 0], (255, 255, 255))
    assert np.array_equal(recolored.pixels[1, 1], (255, 255, 255))

    # пустая палитра → ошибка
    try:
        Converter.mono_to_color(mono_gray, {})
        assert False
    except ValueError as e:
        print("OK: empty palette ->", e)

    #  Статистическая коррекция: Моно → Моно
    ref = MonochromImage(np.array([[0, 50], [100, 255]], dtype=np.uint8))
    hist_ref = Converter._histogram(ref.pixels)

    assert np.isclose(sum(hist_ref.values()), 1.0)

    img = MonochromImage(np.array([[10, 20], [30, 40]], dtype=np.uint8))
    corrected = Converter.mono_to_mono(img, hist=hist_ref)
    print("mono_to_mono (stat):\n", corrected.pixels)

    av1 = sum(k * v for k, v in hist_ref.items())
    assert np.isclose(corrected.pixels.mean(), av1, atol=1e-6)


    #  Статистическая коррекция: Цвет → Цвет
    ref_color = ColorImage([
        np.array([[0, 50], [100, 255]], dtype=np.uint8),
        np.array([[0, 50], [100, 255]], dtype=np.uint8),
        np.array([[0, 50], [100, 255]], dtype=np.uint8),
    ])
    hists = [Converter._histogram(ref_color.pixels[:, :, c]) for c in range(3)]

    img_color = ColorImage([
        np.array([[10, 20], [30, 40]], dtype=np.uint8),
        np.array([[10, 20], [30, 40]], dtype=np.uint8),
        np.array([[10, 20], [30, 40]], dtype=np.uint8),
    ])
    corrected_color = Converter.color_to_color(img_color, hists=hists)
    print("color_to_color (stat):\n", corrected_color.pixels)
    assert corrected_color.shape == (2, 2, 3)

    #  Цвет → Бинарное, Бинарное → Цвет
    color_bin = Converter.color_to_binary(color, 0.5)
    print("color_to_binary:\n", color_bin.pixels)
    assert isinstance(color_bin, BinaryImage)
    assert color_bin.shape == (2, 2)

    color_from_bin = Converter.binary_to_color(b_in, palette)
    print("binary_to_color:\n", color_from_bin.pixels)
    assert isinstance(color_from_bin, ColorImage)
    assert color_from_bin.shape == (2, 2, 3)

    print("=== converter_test passed ===\n")


if __name__ == '__main__':
    print("Program is started \n")

    converter_test()

    print("Program is finished \n")