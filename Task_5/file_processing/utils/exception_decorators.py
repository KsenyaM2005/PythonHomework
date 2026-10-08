def exception_decorator(func):
    def wrapper(*args):
        try:
            return func(*args)
        except BaseException as e:
            print("ОШИБКА !!! {}".format(e))
    return wrapper