from structures.image import get_image_reader
from algorithms.object_analysis import BinaryImage, MonochromeImage, ColorImage
import cv2


def write_data(file_path, data):
    cv2.imwrite(file_path, data)

if __name__ == "__main__":
    bin, mono, color = 0, 1, 2
    reader = get_image_reader(mono)

    path_in = "data/mono.jpg"
    img = reader.read_image(path_in)

    img_analysis = MonochromeImage()

    img_filtered = img_analysis.noise_filtering(img)
    img_segmented, _ = img_analysis.segmentation(img)

    write_data("data/mono_filtered.png", img_filtered)
    write_data("data/mono_segmented.png", img_segmented)