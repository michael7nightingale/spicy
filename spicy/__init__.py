import os

import enums


def Spicy(text: str, type_: str):
    if type_ not in enums.TypeEnum.types.value:
        raise ValueError

    return enums.TypeEnum.types.value[type_](text)


if __name__ == '__main__':
    with open('/'.join(os.getcwd().rsplit('\\')[:-1]) + '/tests/test.html') as file:
        doc = file.read()

    s = Spicy(text=doc, type_='html')
    print(*s.findAll("li", class_='thumbnail-item'))

