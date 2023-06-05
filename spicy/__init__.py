import os
import requests

from .bases import Tag
from .xml_tags import XMLDocument
from .html_tags import HTMLDocument


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

