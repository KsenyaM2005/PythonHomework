import random

from utils.exception_decorators import exception_decorator

# a. Создающая вектор заданной длины N, заполнение – случайные числа от 0..1
@exception_decorator
def randomVec(N):
    return [random.uniform(0,1) for _ in range(N)]

# b. Создающая матрицу MxN, заполнение – случайные числа 0..1
@exception_decorator
def randomMat(M, N):
    return [[random.uniform(0,1) for i in range(N)] for j in range(M)]

# c. Умножающая матрицу на вектор
@exception_decorator
def multMatVec(M, v):
    ans = [0]*len(M)

    for i in range(len(M)):
        row = M[i]
        if len(row) != len(v):
            raise ValueError("Несоответствие размеров!")
        ans[i] = sum([row[j]*v[j] for j in range(len(row))])
    return ans


# e. Печатающую вектор
@exception_decorator
def printVec(v):
    print('[' + "\t".join([str(x) for x in v]) + ']')


# d. Печатающую матрицу
@exception_decorator
def printMat(M):
    print('[')
    for row in M:
        printVec(row)
    print(']')


# f. Находящую сумму диагональных элементов матрицы
@exception_decorator
def sumDiag(M):
    ans = 0
    for i in range(min(len(M), len(M[0]))):
        if len(M[i]) != len(M):
            raise ValueError("Неквадратная матрица!")
        ans += M[i][i]
    return ans

# g. Реализующая двумерную свертку изображения.
@exception_decorator
def conv(M, filter):
    n = len(filter)
    s = len(M) - n + 1

    if s <= 0 or n <= 0 or s > n:
        raise ValueError("Неправильные размерности матриц!")
    ans = [[0] * s for _ in range(s)]

    for i in range(s):
        for j in range(s):
            window = [row[j:j+n] for row in M[i:i+n]]
            ans[i][j] = sum(window[a][b] * filter[a][b]
                            for a in range(n) for b in range(n))
    return ans



if __name__ == '__main__':
    M = randomMat(5, 5)
    printMat(M)
    filter = randomMat(6, 6)
    printMat(filter)
    print()

    printMat(conv(M, filter))


