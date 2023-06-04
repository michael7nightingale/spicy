import os
import requests

from . import enums
from .bases import Tag


def Spicy(text: str, type_: str = 'html') -> Tag:
    if type_ not in enums.TypeEnum.types.value:
        raise ValueError

    return enums.TypeEnum.types.value[type_](text)

