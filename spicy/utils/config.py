from spicy.parser.documents import XMLDocument
from spicy.parser.documents import HTMLDocument, AHTMLDocument


DOCTYPES = {
    "html": HTMLDocument,
    "xml": XMLDocument,

}

ASYNC_DOCTYPES = {
    "html": AHTMLDocument,
    "xml": XMLDocument,

}
