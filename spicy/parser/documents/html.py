from spicy.parser.tags import HTMLTag
from spicy.parser.documents.bases import BaseDocument


class HTMLDocument(BaseDocument):
    __slots__ = ("version", )
    tag = "html"
    tag_type = HTMLTag

    def __init__(self, text: str):
        self.version: int
        self.charset: str
        super().__init__(text)


