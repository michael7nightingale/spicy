import abc
import re
import reprlib
from typing import Any

from tree import Tree, Node


class Tag(abc.ABC):
    """Base tag class."""
    __slots__ = ("tag", "innerText", 'attrs', "id", "is_closed")
    TAG_PATTERN: re.Pattern
    ATTRS_PATTERN: re.Pattern

    def __init__(self, text: Any, is_closed: bool = True):
        self.tag: str
        self.attrs: dict
        self.id: str
        self.is_closed = is_closed
        self.innerText: str = ""
        super().__init__()

    @abc.abstractmethod
    def validateTag(self, tag: Any) -> Any:
        pass

    @abc.abstractmethod
    def validateAttrs(self, attrs: Any) -> Any:
        pass

    @abc.abstractmethod
    def _set_tag(self, text: Any) -> Any:
        pass

    @abc.abstractmethod
    def _find_inner_tags(self, text: Any) -> Any:
        pass

    def __iter__(self):
        return super().__iter__()

    def __len__(self):
        return super().__len__()

    def __str__(self):
        return self.toText()

    def toText(self, layer: int = 0, tab: bool = True, split: str = "\n"):
        """Returns the string object of the tag, incuding all children and tabs"""
        attrs = " ".join((f"{name}={val}" for name, val in self.attrs.items()))
        tab = "\t" if tab else ""
        if self.is_closed:
            text = tab * layer + f"<{self.tag} {attrs}>{split}{self.innerText}{split}"
        else:
            text = tab * layer + f"<{self.tag} {attrs}>{split}"
        for ch in self.children:
            text += ch.toText(layer + 1, tab, split)
        if self.is_closed:
            text += tab * layer + f"</{self.tag}>{split}"
        return text

    def __repr__(self) -> str:
        return reprlib.repr(f"<Tag: {self.tag}, id={self.id}>")


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
        self.tag = self.validateTag(tag)     # tag validation
        del tag

        match_attrs = ATTRS_PATTERN.findall(attrs)
        del attrs

        self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
        if 'class' in self.attrs:
            self.attrs['class_'] = self.attrs['class']
            del self.attrs['class']
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
                    if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
                        yield t


class XMLTag(Tag, Node):
    """XML tag class."""

    def _set_tag(self, text: str):
        pass

    def _find_inner_tags(self, text: Any) -> Any:
        pass

    def validateTag(self, tag: str) -> Any:
        pass

    def validateAttrs(self, attrs: Any) -> Any:
        pass


class BaseDocument(Tag, Tree):
    """Base document class."""

    def _set_tag(self, text: str):
        pass

    def _find_inner_tags(self, text: Any) -> Any:
        pass

    def validateTag(self, tag: str) -> Any:
        pass

    def validateAttrs(self, attrs: Any) -> Any:
        pass

    def _set_document(self, text: Any) -> Any:
        pass


class HTMLDocument(HTMLTag, Tree):
    __slots__ = ()

    def __init__(self, text: str):
        self.meta: list[MetaData] = []
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
            new_meta = MetaData([i[:1] + i[2:] for i in attrs_match])
            self.meta.append(new_meta)

        # setting doctype
        ...


class MetaData:
    attrs: dict

    def __init__(self, attrs):
        self.attrs = dict(attrs)

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __getitem__(self, item):
        return self.attrs[item]


# with open('d:/Progs/PycharmProjects/RepoFastAPI/public/templates/main/layout.html') as file:
#     docs = file.read()

docs = """
<!DOCTYPE html>
<html lang="en">
    <meta charset='utf-8' bios=123>
    <meta parent='id'>
       <a aria-expanded="false" role="button" data-toggle="dropdown" class="dropdown-toggle" href="#">
       Help
       <span class="caret">
       </span>
       </a>
       <div>
        <a aria-expanded="false" role="button" data-toggle="dropdown" class="dropdown-toggle" href="#">
       Help
       </a>
       <span class="caret">
        <h3 id='greeting1'>Hello</h3>
       </div>
        <a aria-expanded="false" role="button" data-toggle="dropdown" class="dropdown-toggle" href="#">
       Help
       </a>
       <span class="caret">
       <script src="//capp.nicepage.com/91ebab354796d476100a0fbf1b762fc8d6d7c384/templates-page-libs.js" defer></script>
 </html>
          """


if __name__ == '__main__':

    el = HTMLDocument(docs)
    print(*el.findAll('a', class_='dropdown-toggle'))
