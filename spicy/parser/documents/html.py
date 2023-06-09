from spicy.parser.tags import HTMLTag, AHTMLTag
from spicy.parser.documents.bases import BaseDocument, BaseADocument


class HTMLDocument(BaseDocument):
    __slots__ = ("version", "charset")
    tag = "html"
    tag_type = HTMLTag

    def __init__(self, text: str,
                 use_threads: bool = False,
                 use_processes: bool = False):
        self.version: int
        self.charset: str
        super().__init__(text,
                         use_threads=use_threads,
                         use_processes=use_processes)


class AHTMLDocument(BaseADocument):
    __slots__ = ("version", "charset")
    tag = "html"
    tag_type = AHTMLTag

    def __init__(self):
        self.version: int
        self.charset: str
        super().__init__()


