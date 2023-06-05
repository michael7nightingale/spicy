from spicy import Spicy
import requests


def test_broad1():
    with open("d:/Progs/PycharmProjects/spicy/tests/test.html",
              encoding='utf-8') as file:
        text = file.read()
    spicy = Spicy(text)
    print(spicy)
    # print(*spicy.findAll('div', class_='button'))


if __name__ == '__main__':
    test_broad1()

