# from spicy.parser.documents.bases import BaseDocument
from spicy.utils.config import DOCTYPES, ASYNC_DOCTYPES
from spicy.utils.exceptions import DoctypeException


def Spicy(text: str,
          doctype: str = 'html',
          use_threads: bool = False,
          use_processes: bool = False):
    """
    __init__() like function, that returns instance of Tag
    depending on what type of document would you like to open.
    """
    doctype = doctype.strip().lower()
    if doctype not in DOCTYPES:  # no matter in which doctype dict, keys are similar
        raise DoctypeException(doctype=doctype)

    if use_processes:
        use_threads = False

    return DOCTYPES[doctype](
        text=text,
        use_threads=use_threads,
        use_processes=use_processes
    )


async def ASpicy(text: str,
           doctype: str = 'html',
           use_threads: bool = False):
    """
     Async version of Spicy.
    """
    doctype = doctype.strip().lower()
    if doctype not in ASYNC_DOCTYPES:  # no matter in which doctype dict, keys are similar
        raise DoctypeException(doctype=doctype)

    aspicy = ASYNC_DOCTYPES[doctype]()
    await aspicy.__ainit__(text)
    return aspicy

async def async_read(filename: str):
    pass


def read(filename: str):
    extension = filename.split(".")[-1]

    with open(filename) as file:
        return Spicy(
            text=file.read(),
            doctype=extension
        )


def read_html(filename: str):
    with open(filename, mode='r') as html_file:
        return Spicy(text=html_file.read())
