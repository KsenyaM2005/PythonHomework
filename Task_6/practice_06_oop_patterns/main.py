from structures.image import get_image_reader, ImgType
from algorithms.object_analysis import BinaryImage, MonochromeImage, ColorImage, get_analysis_object
from structures.histogram import Hist
import cv2


def write_data(file_path, data):
    cv2.imwrite(file_path, data)




def filter_and_segment(img_type, file_path_input, file_filtered, file_segmented):
    reader = get_image_reader(img_type)

    img = reader.read_image(file_path_input)

    img_analysis = get_analysis_object(img_type)

    img_filtered = img_analysis.noise_filtering(img)
    img_segmented, _ = img_analysis.segmentation(img)

    write_data(file_filtered, img_filtered)
    write_data(file_segmented, img_segmented)


if __name__ == "__main__":
    # MONO + read_image
    filter_and_segment(
        ImgType.MONO,
        "data/mono.jpg",
        "data/mono_filtered.png",
        "data/mono_segmented.png"
    )


    # COLOR + read_image
    filter_and_segment(
        ImgType.COLOR,
        "data/color.jpeg",
        "data/color_filtered.png",
        "data/color_segmented.png"
    )

    # Decoder + Encoder + Hist
    hist = Hist.read('data/csv_test.csv')
    data = hist.get_data()

    Hist.write(data, 'data/hist.txt')
    Hist.write(data, 'data/hist.bin')
    Hist.write(data, 'data/hist.json')
    Hist.write(data, 'data/hist.png')