from spicy import Spicy


def test_xml():
    with open("d:/Progs/PycharmProjects/spicy/tests/test.xml",
              encoding='utf-8') as file:
        text = file.read()

    spicy = Spicy(text, type_='xml')
    print(set(spicy.findAll('genre')))


if __name__ == '__main__':
    test_xml()
