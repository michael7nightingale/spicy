from spicy import Spicy


def test_main_functions():
    with open("tests/docs/html/test_broad1.html") as file:
        html_text = file.read()
    spicy = Spicy(
        text=html_text,
    )
    assert spicy.tag == 'html'
    assert len(spicy.children) == 2

    head, body = spicy.children
    assert head.tag == 'head'
    assert len(head.children) == 5
    title, meta1, meta2, meta3, style = head.children
    assert title.tag == 'title'
    assert title.innerText == 'Example Domain'

    assert meta1.tag == meta2.tag == meta3.tag == "meta"
    assert style.tag == 'style'

    assert style.innerText == """body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
        
    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 2em;
        background-color: #fdfdff;
        border-radius: 0.5em;
        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        div {
            margin: 0 auto;
            width: auto;
        }
    }"""

    assert meta1.attributes == {"charset": "utf-8"}
    assert meta3.attributes == {"name": "viewport", 'content': "width=device-width, initial-scale=1"}
    assert meta2.attributes == {"http-equiv": "Content-type", "content": "text/html; charset=utf-8"}
    assert len(body.children) == 1
    div, *_ = body.children
    assert len(div.children) == 3
    h_1, p1, p2 = div.children

    assert h_1.tag == "h1"
    assert h_1.innerText == "Example Domain"
    assert len(p1.children) == 0
    assert p1.innerText == """This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission."""
    assert len(p2.children) == 1
    assert p2.innerText == ""
    a, *_ = p2.children
    assert a.innerText == "More information..."
    assert a.attributes == {"href": "https://www.iana.org/domains/example"}


def test_comment_tag():
    with open("tests/docs/html/test_comment.html") as file:
        html_text = file.read()

    spicy = Spicy(
        text=html_text
    )
    assert spicy
    assert len(list(spicy.iterChildren())) == 4
    head, body = spicy.children
    assert body.innerText == ""
    assert len(head.children) == 2
    meta, title = head.children
    assert meta.attributes == {"charset": "UTF-8"}
    print(meta)
    assert meta.isClosed == False


def test_search():
    with open('tests/docs/html/test_broad2.html', encoding="utf-8") as file:
        html_text = file.read()

    spicy = Spicy(
        html_text,

    )
    assert spicy
    section = spicy.getElementById('main-section')
    assert section.tag == "section"
    assert section.id == "main-section"

    list_search_meta = spicy.findAll("meta")
    assert len(list_search_meta) == 9
    assert all(i.tag == "meta" for i in list_search_meta)
    assert list_search_meta[-1].attributes == {"property": "og:type", "content": "website"}
    assert list_search_meta[0].attributes == {"name": 'hmac-token-name', "content": 'Ajax-Token'}
