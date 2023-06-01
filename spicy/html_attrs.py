from bases import BaseAttribute


class Style(BaseAttribute):
    tag = 'style'

    def setColor(self, color: str) -> None:
        self['color'] = color

    def setSize(self, w: str, h: str) -> None:
        if w != '_':
            self['width'] = w
        if h != '_':
            self['height'] = h


class Meta(BaseAttribute):
    tag = 'meta'

    def setCharset(self, charset: str) -> None:
        self['charset'] = charset


class Link(BaseAttribute):
    tag = 'link'

    def setHref(self, href: str) -> None:
        self['href'] = href
