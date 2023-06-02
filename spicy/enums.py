import enum
from html_tags import HTMLDocument


class TypeEnum(enum.Enum):
    types = {"html": HTMLDocument, 'xml':  BaseException}
