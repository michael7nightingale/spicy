from spicy.parser.tags import XMLTag
from spicy.parser.documents.bases import BaseDocument


class XMLDocument(BaseDocument):
    __slots__ = ()
    tag_type = XMLTag
    tag = "html"

    def __init__(self, text: str):
        super().__init__(text)

        # super calls _set_tag() before
