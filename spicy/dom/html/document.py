from .tag import HTMLTag
from ..base.document import BaseDocument


class HTMLDocument(BaseDocument):
    __slots__ = ("version", "charset")
    tag = "html"
    tagType = HTMLTag

    def __init__(self, text: str,
                 use_threads: bool = False,
                 use_processes: bool = False):
        self.version: int
        self.charset: str
        super().__init__(
            text,
            use_threads=use_threads,
            use_processes=use_processes
        )

    def findIter(self, tag_name, className: str | None = None, **kwargs):
        for el in self.iterChildren():
            if el.tag == tag_name:
                if className is not None:
                    if el.className != className:
                        continue
                if kwargs is not None:
                    if not all(i in self.attributes.items() for i in kwargs.items()):
                        continue
                yield el

    def findAll(self, tag_name, className: str | None = None, **kwargs) -> list:
        result = []
        for el in self.iterChildren():
            if el.tag == tag_name:
                if className is not None:
                    if el.className != className:
                        continue
                if kwargs is not None:
                    if not all(i in self.attributes.items() for i in kwargs.items()):
                        continue
                result.append(el)
        return result

    def findFirst(self, tag_name, className: str | None = None, **kwargs) -> HTMLTag | None:
        for el in self.iterChildren():
            if el.tag == tag_name:
                if className is not None:
                    if el.className != className:
                        continue
                if kwargs is not None:
                    if not all(kwargs[k] == self.attributes.get(k) for k in kwargs):
                        continue
                return el

    def findLast(self, tag_name, className: str | None = None, **kwargs) -> HTMLTag | None:
        result = None
        for el in self.iterChildren():
            if el.tag == tag_name:
                if className is not None:
                    if el.className != className:
                        continue
                if kwargs is not None:
                    if not all(kwargs[k] == self.attributes.get(k) for k in kwargs):
                        continue
                result = el
        return result

    def getAllText(self) -> str:
        return "\n".join(tag.innerText for tag in self)


# class AHTMLDocument(BaseADocument):
#     __slots__ = ("version", "charset")
#     tag = "html"
#     tagType = AHTMLTag
#
#     def __init__(self):
#         self.version: int
#         self.charset: str
#         super().__init__()
