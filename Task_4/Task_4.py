from abc import ABC, abstractmethod
import random


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.myNumber = None

        self.lastVariantNumber = None
        self.victory = False

    @abstractmethod
    def setNumberRange(self, Min, Max):
        ...

    @abstractmethod
    def createNumber(self):
        ...

    @abstractmethod
    def guessNumberStep(self):
        ...

    @abstractmethod
    def updateConditions(self, sign):
        ...

    @abstractmethod
    def giveEstimationForAnswer(self, guessedNumber):
        ...


class Bot(Player):
    def __init__(self, name):
        super().__init__(name)

    def setNumberRange(self, Min, Max):
        self.min = Min
        self.max = Max

    def createNumber(self):
        self.myNumber = random.randint(self.min, self.max)
        return self.myNumber

    def guessNumberStep(self):
        self.lastVariantNumber = (self.min + self.max) // 2
        return self.lastVariantNumber


    def updateConditions(self, sign):
        # sign - загаданное число больше/меньше/равно последнему варианту
        # м.б. < 0, > 0, == 0
        if sign == '<':
            self.max = self.lastVariantNumber - 1
        elif sign == '>':
            self.min = self.lastVariantNumber + 1
        elif sign == '=':
            self.victory = True

    def giveEstimationForAnswer(self, guessedNumber):
        # returns:
        # * < - если загаданное число меньше предложенного
        # * > - если загаданное число больше предложенного
        # * = - если угадано
        if self.myNumber == guessedNumber:
            return '='
        elif self.myNumber < guessedNumber:
            return '<'
        else:
            return '>'

class Human(Player):
    def setNumberRange(self, Min, Max):
        self.min = Min
        self.max = Max
        print("Минимальное значение диапазона: {}".format(Min))
        print("Максимальное значение диапазона: {}".format(Max))

    def createNumber(self):
        print("Загадайте любое число в указанной диапазоне: [{}, {}]:".format(self.min, self.max))
        a = int(input())
        while a < self.min or a > self.max:
            print("Число не соответсвует диапазону. Введите ещё раз:")
            a = int(input())
        self.myNumber = a

        print("ИГРА НАЧАЛАСЬ")
        return self.myNumber

    def guessNumberStep(self):
        print("Введите свой вариант числа противника: целое число")
        self.lastVariantNumber = int(input())
        return self.lastVariantNumber


    def updateConditions(self, sign):
        # sign - загаданное число больше/меньше/равно последнему варианту
        # м.б. < 0, > 0, == 0
        if sign == '<':
            print("Загаданное число меньше вашего последнего варианта")
        elif sign == '>':
            print("Загаданное число больше вашего последнего варианта")
        elif sign == '=':
            print("Поздравляю! Вы угадали")
            self.victory = True

    def giveEstimationForAnswer(self, guessedNumber):
        print('Противник ответил: {}'.format(guessedNumber))
        print(
            'Введите знак, соответствующий тому, загаданное ВАМИ число меньше(<), равно(=) или больше предложенного(>)')
        sign = input()

        while True:
            if sign not in ['<', '=', '>']:
                print('Введите один из предложенных знаков: <, =, >')
                sign = input()
                continue

            if guessedNumber == self.myNumber and sign != '=':
                print('Неверно: числа совпали, нужно ввести =')
            elif guessedNumber > self.myNumber and sign != '<':
                print('Неверно: предложенное число меньше загаданного, нужно ввести <')
            elif guessedNumber < self.myNumber and sign != '>':
                print('Неверно: предложенное число больше загаданного, нужно ввести >')
            else:
                break

            sign = input()

        return sign

class Meneger:
    def __init__(self, K, numberRange):
        self.numberRange = numberRange
        self.K = K

    def play(self, player1, player2):
        player1.setNumberRange(self.numberRange[0], self.numberRange[1])
        player2.setNumberRange(self.numberRange[0], self.numberRange[1])

        player1.createNumber()
        player2.createNumber()

        for i in range(self.K):
            a1 = player1.guessNumberStep()
            sign2 = player2.giveEstimationForAnswer(a1)
            player1.updateConditions(sign2)

            if player1.victory:
                print("Победил", player1.name, "на шаге", i + 1)
                return

            a2 = player2.guessNumberStep()
            sign1 = player1.giveEstimationForAnswer(a2)
            player2.updateConditions(sign1)

            if player2.victory:
                print("Победил", player2.name, "на шаге", i + 1)
                return
            print('\n')

        d1 = abs(player1.lastVariantNumber - player1.myNumber)
        d2 = abs(player2.lastVariantNumber - player2.myNumber)

        if d1 < d2:
            print("Победил", player1.name, "по расстоянию")
        elif d2 < d1:
            print("Победил", player2.name, "по расстоянию")
        else:
            print("Ничья")


if __name__ == '__main__':
    meneger = Meneger(5, [0, 100])
    bot = Bot("bot")
    human = Human("human")

    meneger.play(bot, human)