import re

from .bases import Tag
from .tree import Node, Tree


class XMLTag(Tag, Node):
    """XML tag class."""
    __slots__ = ("tag", "innerText", 'attrs')

    def __init__(self, text: str):
        super().__init__(text)
        self._set_tag(text)

    def _set_tag(self, text: str, parent=None):
        XMLPattern = re.compile(r"<?xml\s+version=(?P<comma>[\"\'])?([\.\d]+)(?P=comma)?\?>")
        ATTRS_PATTERN = re.compile(r"(?P<name>[\-_\w]*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[0-9a-zA-Z-:_;,./ ]*)(?P=comma)?")
        TAG_PATTERN = re.compile(r'<(?P<tag>[\w\-_]+)(?P<attrs>[^>]*)>(?P<inner_tags>.*)</\1>', re.DOTALL)
        if parent is None:  # set parent after the simple call
            parent = self
        if isinstance(parent, Tree):
            version = float(XMLPattern.findall(text)[0][1])
            if not version:
                raise ValueError("Xml version is required.")

        match_text = TAG_PATTERN.findall(text)
        tag, attrs, inner = match_text[0]

        self.tag = self.validateTag(tag)     # tag validation
        del tag

        match_attrs = ATTRS_PATTERN.findall(attrs)
        del attrs
        self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])

        inner_tags, inner_text = self._find_inner_tags(inner)
        self.innerText = inner_text
        for t in inner_tags:
            child = XMLTag(t)
            child.parent = parent
            parent.addChild(child)

    def _find_inner_tags(self, text: str) -> tuple[list[str], str]:
        pattern = re.compile(r"(<([/\-_\w]+)[^>]*>)")
        tag_stack = []
        inner_tags = []
        last_inner_tag = ''
        tag = pattern.search(text)

        while tag:
            tag_beginning, tag_name = tag.groups()
            idx = text.index(tag_beginning)

            if '/' in tag_name:
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

    def validateTag(self, tag: str):
        if tag:
            return tag
        else:
            raise ValueError("Tag is not valid! (it is empty)")

    def validateAttrs(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except:
            raise AttributeError("Attributes are not valid")

    def findAll(self, tag_name, **kwargs):
        for t in self:
            if t.tag == tag_name:
                if not kwargs:
                    yield t
                else:
                    if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
                        yield t


class XMLDocument(XMLTag, Tree):
    __slots__ = ()

    def __init__(self, text: str):
        self.doctype: str
        self.charset: str
        super().__init__(text)

        # super calls _set_tag() before

