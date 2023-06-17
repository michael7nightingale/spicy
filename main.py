from spicy import Spicy, ASpicy
from urllib.request import Request, urlopen
import asyncio


def html():
    request = Request(url='https://example.com/')
    with urlopen(request) as response:
        html_text = response.read().decode(encoding='utf-8')

    spicy = Spicy(
        text=html_text,
        doctype='html',
    )
    print(spicy.tag)    # html
    print(spicy.children)
    print(spicy)


html()


async def async_test_html():
    request = Request(url='https://example.com/')
    with urlopen(request) as response:
        html_text = response.read().decode(encoding='utf-8')

    spicy = await ASpicy(
        text=html_text,
        doctype='html',
    )
    print(spicy.tag)    # html
    print(spicy.children)
    print(spicy)


# asyncio.run(async_test_html())

