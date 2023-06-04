import enum
from .html_tags import HTMLDocument
from .xml_tags import XMLDocument


class TypeEnum(enum.Enum):
    types = {"html": HTMLDocument, 'xml':  XMLDocument}
