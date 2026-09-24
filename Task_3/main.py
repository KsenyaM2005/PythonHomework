# 2. Выполните измерение времени работы реализованных функций для данных
#    различных размерностей, результаты измерений сохраните в файл.

import time
import random

import mats_vectors as mv


def randomVec(N):
    return [random.randint(1, 100) for _ in range(N)]

# b. Создающая матрицу MxN, заполнение – случайные числа 0..1
def randomMat(M, N):
    return [[random.randint(1, 100) for i in range(N)] for j in range(M)]

def decoratorTestMeasureFunc(func):
    def wrapper(*args):
        # print(f'Измеряем время функции: {func.__name__}')
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        # print('\n')

        return result, end-start

    return wrapper


if __name__ == '__main__':
    # Замечание: результаты будут записываться в файл в формате "размер входа: время"
    file = open('times.txt', 'w')
    # a. Умножение «матрица - матрица»

    file.write("# a. Mult Mat x Mat»\n")
    for k in range(2,100,5):
        m1 = randomMat(k,k)
        m2 = randomMat(k,k)

        res, t = decoratorTestMeasureFunc(mv.multMats)(m1, m2)
        file.write(str(k) + ":\t" + str(t) + '\n')

    file.write("\n\n\n")

    # b. Умножение «матрица - вектор»

    file.write("# b. Mult Mat x Vec\n")
    for k in range(2,100,5):
        m = randomMat(k,k)
        v = randomVec(k)

        res, t = decoratorTestMeasureFunc(mv.multMatVec)(m, v)
        file.write(str(k) + ":\t" + str(t) + '\n')

    file.write("\n\n\n")

    # c. Расчет следа матрицы
    file.write("# c. Mat Sp\n")
    for k in range(2,100,5):
        m = randomMat(k,k)

        res, t = decoratorTestMeasureFunc(mv.space)(m)
        file.write(str(k) + ":\t" + str(t) + '\n')

    file.write("\n\n\n")

    # d. Скалярное произведение двух векторов
    file.write("# d. Dot Vec x Vec\n")
    for k in range(2,100,5):
        v1 = randomVec(k)
        v2 = randomVec(k)

        res, t = decoratorTestMeasureFunc(mv.dot)(v1,v2)
        file.write(str(k) + ":\t" + str(t) + '\n')

    file.write("\n\n\n")

    # e. Расчет гистограммы для вектора с изменяемым количеством квантов
    file.write("# e. Histogram\n")
    for k in range(2,100,5):
        v = randomVec(k)

        res, t = decoratorTestMeasureFunc(mv.histogram)(v,10)
        file.write(str(k) + ":\t" + str(t) + '\n')

    file.write("\n\n\n")

    # f. Фильтрация вектора ядерным фильтром (например, [-1, 0, 1] – приближенное вычисление градиента данных)
    file.write("# f. Filter\n")
    for k in range(5,100,5):
        v = randomVec(k)
        f = randomVec(3)

        res, t = decoratorTestMeasureFunc(mv.conv1D)(v, f)
        file.write(str(k) + ":\t" + str(t) + '\n')

    file.write("\n\n\n")


    file.close()

