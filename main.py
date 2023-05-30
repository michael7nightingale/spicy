import abc
import re


class HTMLElementBase(abc.ABC):
    __slots__ = ("tag", "innerText", "class_", "id", "children", "context", 'attrs')
    tag_pattern: re.Pattern
    attrs_pattern: re.Pattern

    def __init__(self, document: str) -> None:
        self.content: str = document
        self.tag: str
        self.attrs: dict
        self.innerText: str
        self.class_: str
        self.id: str
        self.children: list

        self._set_attributes(self.content)


class Attributable(abc.ABC):

    @abc.abstractmethod
    def _set_attributes(self, text: str):
        pass


class ReprMixin:
    content: str

    def __repr__(self):
        return self.content


class HTMLElement(ReprMixin, HTMLElementBase):
    attrs_pattern = re.compile(r"(\w*)\s*?=\s*?[\"\']?([\w\s]*)[\"\']?")
    tag_pattern = re.compile(r"<(\w*)(.*)>([\s\S]*)</\w*>")

    def _set_attributes(self, text: str):
        fill_unstated = None

        tag, attrs, inner = self.tag_pattern.findall(text)[0]
        # print(tag, attrs, inner)

        stripped_tag = tag.strip()
        if not stripped_tag:
            raise ValueError("Tag is not correct")
        self.tag = stripped_tag
        del tag, stripped_tag

        attrs_items = self.attrs_pattern.findall(attrs)
        self.attrs = dict(attrs_items)
        self.id = self.attrs.get('id', fill_unstated)
        self.class_ = self.attrs.get('class', fill_unstated)

        innerText_pattern = re.compile(r'[\w\W]*(?=<)')

        # print(innerText_pattern.findall(inner))
        # self.innerText =


class HTMLDocument(ReprMixin, Attributable):
    attrs_pattern = re.compile(r"(\w*)\s*?=\s*?[\"\']?([\w\s]*)[\"\']?")
    tag_pattern = re.compile(r"<(?!DOCTYPE)(\w*)(.*)>([\s\S]*)</\w*>")

    def __init__(self, text: str):
        self.content = text
        self.meta: dict
        self.doctype: dict
        self.children: dict

        self._set_attributes(self.content)

    def _set_attributes(self, text: str):
        fill_unstated = None
        doctype_pattern = re.compile(r"<!DOCTYPE\s*(\w*)\s*>")
        tag, attrs, inner = self.tag_pattern.findall(text)[0]
        print(123, tag)
        doctype = doctype_pattern.findall(text)
        print(doctype)

        if tag != "html":
            raise ValueError("Tag html is not correct")
        self.tag = tag

        del tag

        attrs_items = self.attrs_pattern.findall(attrs)
        self.attrs = dict(attrs_items)
        self.id = self.attrs.get('id', fill_unstated)
        self.class_ = self.attrs.get('class', fill_unstated)


with open('d:/Progs/PycharmProjects/RepoFastAPI/public/templates/main/layout.html') as file:
    docs = file.read()

docs = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My Django Application</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

</head>

<body>
   
</body>
</html>
"""

html = HTMLDocument(docs)
