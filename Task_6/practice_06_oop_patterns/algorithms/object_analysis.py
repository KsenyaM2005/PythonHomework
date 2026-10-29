"""
Шаблонный метод (Template method)
"""
import cv2
import numpy as np

from structures.image import ImgType

class ObjectAnalysis(object):
    def template_method(self, image):

        image = self.noise_filtering(image)
        data = self.segmentation(image)
        data = self.object_parameters(data)

        return data

    def noise_filtering(self, image):
        raise NotImplementedError()

    def segmentation(self, data):
        raise NotImplementedError()

    def object_parameters(self, data):
        (image, data) = data
        (numLabels, labels, stats, centroids) = data
        x = []
        y = []
        w = []
        h = []
        area = []
        hu = []

        for i in range(1, numLabels):
            x.append(stats[i, cv2.CC_STAT_LEFT])
            y.append(stats[i, cv2.CC_STAT_TOP])
            w.append(stats[i, cv2.CC_STAT_WIDTH])
            h.append(stats[i, cv2.CC_STAT_HEIGHT])
            area.append(stats[i, cv2.CC_STAT_AREA])

            # Hu-moments
            mask = (labels == i).astype(np.uint8) * 255
            m = cv2.moments(mask)
            hu_vec = cv2.HuMoments(m).flatten()
            hu.append(hu_vec)

        return (x, y, w, h, area, hu)


class BinaryImage(ObjectAnalysis):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        median = cv2.medianBlur(image, 5)
        return median

    def segmentation(self, image):
        output = cv2.connectedComponentsWithStats(
            image,
            4, # connectivity
            cv2.CV_32S)
        return (image, output)

class MonochromeImage(BinaryImage):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        # фильтр Гаусса
        dst = cv2.GaussianBlur(image, (5, 5), 0)
        return dst

    def segmentation(self, image):
        # границы
        edges = cv2.Canny(image,100,200)
        # разметка связных компонент
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            edges,
            4,
            cv2.CV_32S
        )
        output = (num_labels, labels, stats, centroids)
        return edges, output

class ColorImage(MonochromeImage):
    def __init__(self):
        self.rng = np.random.default_rng()

    def noise_filtering(self, image):
        # фильтр Гаусса
        dst = cv2.GaussianBlur(image, (5, 5), 0)
        return dst

    def segmentation(self, image):
        # Конвертация в монохром
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Подготовка: белый фон -> чёрный
        img_proc = image.copy()
        white_mask = np.all(img_proc == 255, axis=2)
        img_proc[white_mask] = 0

        # Laplacian sharpening
        kernel = np.array([[1, 1, 1],
                           [1, -8, 1],
                           [1, 1, 1]], dtype=np.float32)

        img_laplacian = cv2.filter2D(img_proc, cv2.CV_32F, kernel)
        sharp = np.float32(img_proc)
        img_result = sharp - img_laplacian

        # Обратно в 8-бит
        img_result = np.clip(img_result, 0, 255).astype(np.uint8)

        # Бинаризация (Otsu) по градациям серого
        bw_gray = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(bw_gray, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Distance Transform
        dist = cv2.distanceTransform(bw, cv2.DIST_L2, 3)
        cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)

        # Порог для получения "пиков"/центроидов
        _, dist = cv2.threshold(dist, 0.4, 1.0, cv2.THRESH_BINARY)

        # Небольшая дилатация центроидов
        kernel1 = np.ones((3, 3), dtype=np.uint8)
        dist = cv2.dilate(dist, kernel1)

        # Поиск контуров по пикам
        dist_8u = dist.astype(np.uint8)
        contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None

        # Маркеры для Watershed
        markers = np.zeros(dist.shape, dtype=np.int32)
        for i, cnt in enumerate(contours):
            cv2.drawContours(markers, contours, i, (i + 1), -1)

        # Маркер фона
        cv2.circle(markers, (5, 5), 3, 255, -1)

        # Watershed
        cv2.watershed(img_result, markers)

        # Постобработка меток:
        #     -1 (границы) -> 0 (фон)
        #    255 (маркер фона) -> 0
        labels = markers.copy()
        labels[labels == -1] = 0
        labels[labels == 255] = 0

        # Перенумерация 1..N
        unique_labels = np.unique(labels)
        unique_labels = unique_labels[unique_labels > 0]
        num_labels = len(unique_labels)

        label_map = {old: new for new, old in enumerate(unique_labels, start=1)}
        for old_lbl, new_lbl in label_map.items():
            labels[labels == old_lbl] = new_lbl

        # outputs
        stats_list = []
        centroids_list = []

        for lbl in range(1, num_labels + 1):
            mask = (labels == lbl).astype(np.uint8) * 255
            x, y, ww, hh = cv2.boundingRect(mask)
            area = cv2.countNonZero(mask)

            M = cv2.moments(mask)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = x + ww // 2, y + hh // 2

            stats_list.append([x, y, ww, hh, area])
            centroids_list.append([cx, cy])

        stats = np.array(stats_list, dtype=int)
        centroids = np.array(centroids_list, dtype=float)

        # Цветное сегментированное изображение
        seg_image = np.zeros_like(image)
        colors = [(int(self.rng.integers(0, 256)),
                   int(self.rng.integers(0, 256)),
                   int(self.rng.integers(0, 256))) for _ in range(num_labels)]

        for lbl in range(1, num_labels + 1):
            seg_image[labels == lbl] = colors[lbl - 1]

        output = (num_labels, labels, stats, centroids)
        return seg_image, output



"""
Декоратор - структурный паттерн
"""

class FilteredAnalysis(ObjectAnalysis):
    def __init__(self, obj):
        self._proc = obj

    def template_method(self, image):
        (_x, _y, _w, _h, _area, _hu) = self._proc.template_method(image)

        x, y, w, h, area, hu = [], [], [], [], [], []

        for i in range(len(_area)):
            if 10 < _area[i] < 2500:
                x.append(_x[i])
                y.append(_y[i])
                w.append(_w[i])
                h.append(_h[i])
                area.append(_area[i])
                hu.append(_hu[i])

        return (x, y, w, h, area, hu)


def get_analysis_object(ident):
    if ident == 0 or ident == ImgType.BIN:
        return BinaryImage()
    elif ident == 1 or ident == ImgType.MONO:
        return MonochromeImage()
    elif ident == 2 or ident == ImgType.COLOR:
        return ColorImage()


if __name__== '__main__':
    print("Binary Image Processing")
    bin_segm = BinaryImage()
    (x,y,w,h,area) = bin_segm.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])

    print("Decorated Binary Image Processing")
    filt_bin = FilteredAnalysis(BinaryImage())
    (x, y, w, h, area) = filt_bin.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])
