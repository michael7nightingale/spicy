import re
from typing import Any

from bases import Tag
from tree import Node, Tree
from html_attrs import Link, Style, Meta


class HTMLTag(Tag, Node):
    """HTML tag class."""
    __slots__ = ("class_", "style")

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

    def _find_inner_tags(self, text: str) -> list[str]:
        TAGS_PATTERN = re.compile(r"(<(?P<tag>\w*).*>[\s\S]*</(?P=tag)>)")

        if text.strip():
            match = TAGS_PATTERN.findall(text)
            return [i[0] for i in match]

    def validateAttrs(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except:
            raise AttributeError("Attributes are not ovalid")

    def _set_tag(self, text: str, parent=None):
        FILL_UNSTATED_WITH = None
        ATTRS_PATTERN = re.compile(r"(?P<name>\w*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[0-9a-zA-Z-:_;,./]*)(?P=comma)?")
        TAG_PATTERN = re.compile(r"<(?P<tag>\w*)(?P<attrs>.*)>(?P<inner>[\s\S]*)</(?P=tag)>")
        if parent is None:  # set parent after the simple call
            parent = self

        match_text = TAG_PATTERN.findall(text)

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
        inner_tags = self._find_inner_tags(inner)
        # print(inner_tags)
        if inner_tags:
            for t in inner_tags:
                child = HTMLTag(t)
                child.parent = parent
                parent.addChild(child)

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
    __slots__ = ()

    def __init__(self, text: str):
        self.meta: list[Meta] = []
        self.doctype: str
        self.charset: str
        self.content: str = text
        super().__init__(text)

        # super calls _set_tag() before
        self._set_document(text)

    def _set_document(self, text: Any) -> Any:
        # setting metadata
        ATTRS_PATTERN: re.Pattern = re.compile(r"(?P<name>\w*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[0-9a-zA-Z-:_;,./]*)(?P=comma)?")
        META_PATTERN: re.Pattern = re.compile(f"<meta\s*(.*?)\s*>")

        match_meta = META_PATTERN.findall(text)
        for el in match_meta:
            attrs_match = ATTRS_PATTERN.findall(el)
            new_meta = Meta([i[:1] + i[2:] for i in attrs_match])
            self.meta.append(new_meta)

        # setting doctype
        ...

