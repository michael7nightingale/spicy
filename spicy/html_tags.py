import re
from typing import Type

from .bases import Tag, BaseAttribute
from .tree import Node, Tree
from .html_attrs import Link, Style, Meta, Image


attributes_classes: dict[str, Type[BaseAttribute]] = {
    "style": Style,
    "meta": Meta,
    "link": Link,
    "img": Image,

    "path": Image,
    "base": Image,
    "hr": Image,
    # "header": Image
    "br": Image,
    "input": Image,

}


class HTMLTag(Tag, Node):
    """HTML tag class."""
    __slots__ = ("class_", "style", "tag", "innerText", 'attrs', "id", "is_closed")

    def __init__(self, text: str):
        super().__init__(text)
        self.class_: str
        self.style: str
        self._set_tag(text)

    def validateTag(self, tag: str):
        if tag:
            return tag
        else:
            raise ValueError("Tag is not valid! (it is empty)")

    def _find_inner_tags(self, text: str) -> tuple[list[str], str]:
        pattern = re.compile(r"(<([/\-_\w]+)[^>]*>)")
        tag_stack = []
        inner_tags = []
        unclosed_tags = []
        last_inner_tag = ''
        tag = pattern.search(text)

        while tag:
            tag_beginning, tag_name = tag.groups()
            idx = text.index(tag_beginning)
            if tag_name in attributes_classes:
                # from_replace_idx = idx
                last_inner_tag += tag_beginning
                unclosed_tags.append(tag_beginning)
                text = text.replace(tag_beginning, '', 1)

            elif '/' in tag_name:
                last_inner_tag += text[from_replace_idx:idx + len(tag_beginning)]
                text = text[:from_replace_idx] + text[idx + len(tag_beginning):]
                last_stack_tag = tag_stack[-1]
                if tag_name.replace('/', '') == last_stack_tag:
                    tag_stack.pop()
            else:
                from_replace_idx = idx
                last_inner_tag += tag_beginning
                text = text.replace(tag_beginning, '', 1)
                tag_stack.append(tag_name)

            if not tag_stack:
                inner_tags.append(last_inner_tag)
                last_inner_tag = ''

            tag = pattern.search(text)
        return inner_tags, text.strip()

    def validateAttrs(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except:
            raise AttributeError("Attributes are not valid")

    def _set_tag(self, text: str, parent=None):
        FILL_UNSTATED_WITH = None
        ATTRS_PATTERN = re.compile(r"(?P<name>[\-_\w]*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[0-9a-zA-Z-:_;,./ ]*)(?P=comma)?")
        TAG_PATTERN = re.compile(r'<(?P<tag>[\w\-_]+)(?P<attrs>[^>]*)>(?P<inner_tags>.*)</\1>', re.DOTALL)
        if parent is None:  # set parent after the simple call
            parent = self

        if text.count('<') > 1:
            match_text = TAG_PATTERN.findall(text)
            # print(text)
            tag, attrs, inner = match_text[0]
            if isinstance(parent, Tree):
                if tag != 'html':
                    raise ValueError("Html tag is required!")
            self.tag = self.validateTag(tag)     # tag validation

            del tag
            match_attrs = ATTRS_PATTERN.findall(attrs)
            del attrs

            self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
            self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
            self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)

            inner_tags, inner_text = self._find_inner_tags(inner)
            self.innerText = inner_text
            for t in inner_tags:
                child = HTMLTag(t)
                child.parent = parent
                parent.addChild(child)

        else:
            ATTRIBUTE_PATTERN: re.Pattern = re.compile(r"<(\w*)\s*(.*?)>")
            match_text = ATTRIBUTE_PATTERN.findall(text)
            tag, attrs = match_text[0]
            self.tag = tag
            self.is_closed = False
            match_attrs = ATTRS_PATTERN.findall(attrs)
            del attrs

            self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
            self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
            self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)

    def findAll(self, tag_name, **kwargs):
        for t in self:
            if t.tag == tag_name:
                if not kwargs:
                    yield t
                else:
                    if 'class_' in kwargs:
                        kwargs['class'] = kwargs['class_']
                        del kwargs['class_']
                    if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
                        yield t


class HTMLDocument(HTMLTag, Tree):
    __slots__ = ("version", )

    def __init__(self, text: str):
        self.meta: list[Meta] = []
        self.version: int
        self.charset: str
        super().__init__(text)

        # super calls _set_tag() before
