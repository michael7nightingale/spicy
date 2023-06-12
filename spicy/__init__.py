from spicy.parser.tags.bases import Tag
from spicy.parser.tags import XMLDocument
from spicy.parser.tags import HTMLDocument


types_ = {
    "html": HTMLDocument,
    "xml": XMLDocument,

}


def Spicy(text: str, type_: str = 'html') -> Tag:
    """
    __init__() like function, that returns instance of Tag
    depending on what type of document would you like to open.
    """
    type_ = type_.strip().lower()
    if type_ not in types_:
        raise ValueError

    return types_[type_](text)
