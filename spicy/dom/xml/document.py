from .tag import XMLTag
from ..base.document import BaseDocument


class XMLDocument(BaseDocument):
    __slots__ = ()
    tag_type = XMLTag
    tag = "html"

    def __init__(self, text: str):
        super().__init__(text)
