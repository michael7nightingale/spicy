from .bases import BaseAttribute
from .tree import Node


class Attribute(BaseAttribute, Node):

    def toText(self, layer: int = 0, tab: bool = True, split: str = '\n'):
        tab = '\t' if tab else ''
        attrs = " ".join(f'{i}=\'{j}\'' for i, j in self._attrs.items())
        return tab * layer + f"<{self.tag} {attrs}>{split}"

    def __str__(self):
        return self.toText()


class Style(Attribute):
    tag = 'style'

    def setColor(self, color: str) -> None:
        self['color'] = color

    def setSize(self, w: str, h: str) -> None:
        if w != '_':
            self['width'] = w
        if h != '_':
            self['height'] = h


class Meta(Attribute):
    tag = 'meta'

    def setCharset(self, charset: str) -> None:
        self['charset'] = charset


class Link(Attribute):
    tag = 'link'

    def setHref(self, href: str) -> None:
        self['href'] = href


class Image(Attribute):
    tag = 'img'
