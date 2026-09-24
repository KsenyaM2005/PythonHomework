# 1. Реализуйте модуль функций, реализующих базовые матрично-векторные операции, операции работы с данными
#   (разместить в отдельном .py файле, вызовы функций реализовать в main, к примеру):
#     a. Умножение «матрица - матрица»
#     b. Умножение «матрица - вектор»
#     c. Расчет следа матрицы
#     d. Скалярное произведение двух векторов
#     e. Расчет гистограммы для вектора с изменяемым количеством квантов
#     f. Фильтрация вектора ядерным фильтром (например, [-1, 0, 1] – приближенное вычисление градиента данных)
#     h. Чтение/запись данных в файл, из файла


# a. Умножение «матрица - матрица»
def multMats(M1, M2):
    ans = [[0]*len(M2[0]) for _ in range(len(M1))]

    for i in range(len(M1)):
        for j in range(len(M2[0])):
            if len(M1[i]) != len(M2) or len(M2[:][j]) != len(M2[:][0]):
                raise ValueError("multMats: Несоответствие размеров!")
            ans[i][j] = sum(M1[i][k] * M2[k][j]
                            for k in range(len(M1[i])))
    return ans

# b. Умножение «матрица - вектор»
def multMatVec(M, v):
    ans = [0]*len(M)

    for i in range(len(M)):
        row = M[i]
        if len(row) != len(v):
            raise ValueError("multMatVec: Несоответствие размеров!")
        ans[i] = sum([row[j]*v[j] for j in range(len(row))])
    return ans


# c. Расчет следа матрицы
def space(M):
    ans = 0
    for i in range(len(M)):
        if i < len(M[i]):
            ans += M[i][i]
    return ans


# d. Скалярное произведение двух векторов
def dot(vec1, vec2):
    ans = 0
    if len(vec1) != len(vec2):
        raise ValueError("dot: Несоответствие размеров!")
    for i in range(len(vec1)):
        ans += vec1[i] * vec2[i]
    return ans


# e. Расчет гистограммы для вектора с изменяемым количеством квантов
def histogram(array, bin_size=10):
    if not array:
        return []

    lo = min(array)
    hi = max(array)

    first = lo + bin_size - (lo + bin_size) % bin_size if (lo + bin_size) % bin_size else lo + bin_size
    last = hi + bin_size - (hi + bin_size) % bin_size

    # Количество бинов и границы
    n_bins = (last - first) // bin_size + 1
    hist = [0] * n_bins
    bounds = [first + i * bin_size for i in range(n_bins)]

    for x in array:
        binIdx = 0
        while binIdx < n_bins - 1 and x >= bounds[binIdx + 1]:
            binIdx += 1
        hist[binIdx] += 1

    return hist


# f. Фильтрация вектора ядерным фильтром (например, [-1, 0, 1] – приближенное вычисление градиента данных)
def conv1D(vec, filter):
    n = len(filter)
    s = len(vec) - n + 1
    ans = [0] * s

    for i in range(s):
            window = vec[i:i+n]
            ans[i] = sum(window[a] * filter[a] for a in range(n))
    return ans


# h. Чтение/запись данных в файл, из файла
def read(filename):
    f = open(filename, 'r')
    strings = f.readlines()
    if len(strings) == 0:
        return []
    elif len(strings) == 1:
        return list(strings[0].split(' ')[0])
    else:
        ans = [0] * len(strings)
        for i, string in enumerate(strings):
            ans[i] = [string.split(' ')[0]]
    f.close()

    return ans

def write(filename, array):
    f = open(filename, 'w')
    for row in array:
        f.write(" ".join([str(x) for x in row]) + '\n')
    f.close()