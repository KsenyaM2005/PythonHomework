import sys
import argparse

from utils.reader import image_reader as imread
from utils.reader import csv_reader, bin_reader, txt_reader, json_reader
from utils.processor import histogram
from utils.writer import csv_writer, bin_writer, txt_writer, image_writer, json_writer

from utils.image_toner import stat_correction, equalization, gamma_correction


def print_args_1():
    print(type(sys.argv))
    if (len(sys.argv) > 1):
        for param in sys.argv[1:]:
            print(param, type(param))
    return sys.argv[1:]

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-img','--img_path', default ='', help='Path to image')

    parser.add_argument ('-p','--path', default ='', help='Input file path ')

    parser.add_argument('-o', '--output', help='Save file path')

    parser.add_argument('-t', '--transform', default='stat', help='Path to image')

    return parser


def getFormat(path: str) -> str:
    if '.' in path:
        f = path.split('.')[-1]
        if f == 'jpg' or f == 'jpeg' or f == 'png':
            f = 'img'
        return f
    else:
        raise ValueError("В пути файла нет формата!")


def getHistTemplate(path: str):
    hist_template = None

    type = getFormat(path)

    match type:
        case 'img':
            img2 = imread.read_data(path)
            hist_template = histogram.image_processing(img2)
        case 'csv':
            hist_template = csv_reader.read_data(path)
        case 'bin':
            hist_template = bin_reader.read_data(path)
        case 'txt':
            hist_template = txt_reader.read_data(path)
        case 'json':
            hist_template = json_reader.read_data(path)
        case _:
            raise ValueError("Неправильный формат!")
    return hist_template


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args(sys.argv[1:])

    image = imread.read_data(args.img_path)

    option = args.transform

    res_image = None
    match option:
        case 'stat':
            hist_template = getHistTemplate(args.path)
            res_image = stat_correction.processing(hist_template, image)
        case 'equalize':
            res_image = equalization.processing(image)
        case 'gamma':
            res_image = gamma_correction.processing(image)
        case _:
            pass

    image_writer.write_data(args.output, res_image)