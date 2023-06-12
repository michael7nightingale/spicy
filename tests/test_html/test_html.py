from spicy import Spicy
from urllib.request import Request, urlopen


def test_html():
    request = Request(url='https://example.com/')
    with urlopen(request) as response:
        html_text = response.read().decode(encoding='utf-8')

    spicy = Spicy(
        text=html_text,
        type_='html'
    )
    print(spicy.tag)    # html
    print(spicy.children)
    assert not spicy







    # test_broad1()
