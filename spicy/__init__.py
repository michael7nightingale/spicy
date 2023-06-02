import os
import requests

import enums
from bases import Tag


def Spicy(text: str, type_: str) -> Tag:
    if type_ not in enums.TypeEnum.types.value:
        raise ValueError

    return enums.TypeEnum.types.value[type_](text)


if __name__ == '__main__':
    # url = "https://github.com/michael7nightingale"
    # response = requests.get(url)
    with open('d:/Progs/PycharmProjects/spicy/tests/mini-test.html', encoding='utf-8') as f:
        txt = f.read()

    s = Spicy(txt, type_='html')

    with open('d:/Progs/PycharmProjects/spicy/tests/spiced.html', 'w', encoding='utf-8') as f2:
        f2.write(s.toText())

    # print(s)
