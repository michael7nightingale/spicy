from spicy import Spicy


def html():
    with open("tests/docs/html/dnevnik.html", encoding='utf-8') as file:
        html_text = file.read()
    spicy = Spicy(
        text=html_text,
        doctype='html',
    )
    return spicy


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
