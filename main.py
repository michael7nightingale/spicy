from spicy import Spicy
from time import perf_counter


def html():
    # request = Request(url='https://dnevnik.ru/')
    # with urlopen(request) as response:
    #     html_text = response.read().decode(encoding='utf-8')
    with open("tests/docs/html/dnevnik.html", encoding='utf-8') as file:
        html_text = file.read()
    time0 = perf_counter()
    spicy = Spicy(
        text=html_text,
        doctype='html',
        # use_threads=True
    )
    # print(spicy.tag)    # html
    # print(spicy.children)
    print(spicy)
    print(f"Time: {perf_counter() - time0}")


html()


# async def async_html():
#     request = Request(url='https://github.com/')
#     with urlopen(request) as response:
#         html_text = response.read().decode(encoding='utf-8')
#     time0 = perf_counter()
#     spicy = await ASpicy(
#         text=html_text,
#         doctype='html',
#     )
#     print(f"Time: {perf_counter() - time0}")
#     # print(spicy.tag)    # html
#     # print(spicy.children)
#     print(spicy)
#
#
# asyncio.run(async_html())
