import abc
import re
from typing import Any
from reprlib import repr

from .tree import Tree


class Tag(abc.ABC):
    """Base tag class."""
    __slots__ = ("tag", "innerText", 'attrs', "id", "is_closed")
    TAG_PATTERN: re.Pattern
    ATTRS_PATTERN: re.Pattern

    def __init__(self, text: Any, is_closed: bool = True):
        self.tag: str = ''
        self.attrs: dict = {}
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

    @abc.abstractmethod
    def findAll(self, tag_name, **kwargs):
        pass

    def __iter__(self):
        return super().__iter__()

    def __len__(self):
        return super().__len__()

    def __str__(self):
        return self.toText()

    def toText(self, layer: int = 0, tab: bool = True, split: str = "\n"):
        """Returns the string object of the tag, incuding all children and tabs"""
        # print(self.children)
        attrs = " ".join((f"{name}='{val}'" for name, val in self.attrs.items()))
        tab = "  " if tab else ""
        if self.is_closed:
            to_cont = split if self.children else ""
            text = tab * layer + f"<{self.tag} {attrs}>{self.innerText}{to_cont}"
        else:
            text = tab * layer + f"<{self.tag} {attrs}>{split}"
        for ch in self.children:
            text += ch.toText(layer + 1, tab, split)
        if self.is_closed:
            text += tab * layer + f"</{self.tag}>{split}"
        return text

    def __repr__(self) -> str:
        return repr(f"<Tag: {self.tag}, id={self.id}>")


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


class BaseAttribute(abc.ABC):
    __slots__ = ('_attrs', )
    tag: str

    def __init__(self, attrs: dict | list[tuple], **kwargs):
        self._attrs = dict(attrs)
        self._attrs.update(kwargs)
        super().__init__()

    def __setitem__(self, key, value):
        if isinstance(key, str) and isinstance(value, str):
            self._attrs[key] = value
        else:
            raise TypeError

    def __getitem__(self, item):
        return self._attrs[item]
