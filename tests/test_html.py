from spicy import Spicy
import requests


def test_broad1():
    with open("d:/Progs/PycharmProjects/spicy/tests/test_broad1.html",
              encoding='utf-8') as file:
        text = file.read()
    spicy = Spicy(text)
    print(spicy)
    # print(*spicy.findAll('div', class_='button'))


if __name__ == '__main__':
    from spicy import Spicy
    from urllib.request import Request,urlopen

    request = Request(url='https://example.com/')
    with urlopen(request) as response:
        html_text = response.read().decode(encoding='utf-8')

    spicy = Spicy(
        text=html_text,
        type_='html'
    )

    print(spicy.tag)    # html
    print(spicy.children)
    print(spicy)
    # test_broad1()
