import enum
import tags


class TypeEnum(enum.Enum):
    types = {"html": tags.HTMLDocument, 'xml':  BaseException}

