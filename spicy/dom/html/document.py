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


# class AHTMLDocument(BaseADocument):
#     __slots__ = ("version", "charset")
#     tag = "html"
#     tagType = AHTMLTag
#
#     def __init__(self):
#         self.version: int
#         self.charset: str
#         super().__init__()
