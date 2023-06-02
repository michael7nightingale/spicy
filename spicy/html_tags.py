import re
from typing import Any, Type

from bases import Tag, BaseAttribute
from tree import Node, Tree
from html_attrs import Link, Style, Meta, Image


attributes_classes: dict[str, Type[BaseAttribute]] = {
    "style": Style,
    "meta": Meta,
    "link": Link,
    "img": Image,

}


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
        TAGS_PATTERN = re.compile(r"(<(?P<tag>\w*)\s*.*>[\s\S]*</(?P=tag)>)")
        tags = []
        # print(12, text)
        if text.strip():
            # while text:
            #     match = TAGS_PATTERN.search(text)
            #     if match is not None:
            #         # print(123123, match[0])
            #         tags.append(match[0])
            #         text = text.replace(match[0], '', 1)
            #     else:
            #         break
            # attr = self._find_all_attributes(text.strip())
            # if attr is None:
            #     # print(text)
            #     self.innerText = text.strip()
            # else:
            #     self.addChild(attr)
            #     attr.patent = self
            tags = [i[0] for i in TAGS_PATTERN.findall(text)]
            # print(tags)
            return tags

    def _find_all_attributes(self, text: str) -> BaseAttribute:
        ATTRIBUTE_PATTERN: re.Pattern = re.compile(r"<(\w*)\s*(.*?)>")
        match = ATTRIBUTE_PATTERN.findall(text)
        ATTRS_PATTERN: re.Pattern = re.compile(r"([-_\w]*)\s*?=\s*?(?P<comma>[\'\"])([0-9a-zA-Z-_./,:;+\s|]*)(?P=comma)")
        if len(match) > 1:
            return
        if not match:
            return
        tag_name, attr_string = match[0]
        attrs = self.validateAttrs([i[:1] + i[2:] for i in ATTRS_PATTERN.findall(attr_string)])

        attr_class = attributes_classes.get(tag_name)
        if attr_class is None:
            return
        attr_obj = attr_class(attrs)
        return attr_obj

    def validateAttrs(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except:
            raise AttributeError("Attributes are not ovalid")

    def _set_tag(self, text: str, parent=None):
        FILL_UNSTATED_WITH = None
        ATTRS_PATTERN = re.compile(r"(?P<name>[-_\w]*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[0-9a-zA-Z-:_;,./ ]*)(?P=comma)?")
        TAG_PATTERN = re.compile(r"<(?P<tag>\w*)\s*(?P<attrs>.*?)>(?P<inner>[\s\S]*)</(?P=tag)>")
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
        # print(2, inner)
        inner_tags = self._find_inner_tags(inner)
        del inner
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

        # match_meta = META_PATTERN.findall(text)
        # for el in match_meta:
        #     attrs_match = ATTRS_PATTERN.findall(el)
        #     new_meta = Meta([i[:1] + i[2:] for i in attrs_match])
        #     self.meta.append(new_meta)

        # setting doctype
        ...

