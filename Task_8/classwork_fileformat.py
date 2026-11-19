import re


# ОПРЕДЕЛЕНИЕ ФОРМАТА С ПОМОЩЬЮ re
def getFormat(path: str) -> str:
    result = re.search(r"\.(jpg|jpeg|png|csv|txt|bin|json)$", path)

    if result != None:
        result = result.group()[1:]
    if result == "jpg" or result == "jpeg" or result == "png":
        result = "img"
    return result


if __name__ == '__main__':
    print(getFormat("path.png"))
    print(getFormat("path.jpeg"))
    print(getFormat("path.json"))
    print(getFormat("path.csv"))
    print(getFormat("path.bin"))
    print(getFormat("path.txt"))
    print(getFormat("pathtxt"))