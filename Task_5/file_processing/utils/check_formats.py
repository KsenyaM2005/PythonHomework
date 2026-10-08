def getFormat(path: str) -> str:
    if '.' in path:
        f = path.split('.')[-1]
        if f == 'jpg' or f == 'jpeg' or f == 'png':
            f = 'img'
        return f
    else:
        raise ValueError("В пути файла нет формата!")