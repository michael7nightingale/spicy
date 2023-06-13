from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from reprlib import repr

from spicy.tree import Tree


class Tag(ABC):
    """Base tag class."""
    __slots__ = ("tag", "innerText", 'attrs', "id", "is_closed")
    _patterns: Enum

    class Config:
        use_threads = False
        use_processes = False

    def __init__(self,
                 text: Any,
                 is_closed: bool = True,
                 use_threads: bool = False,
                 use_processes: bool = False):
        self.tag: str = ''
        self.attrs: dict = {}
        self.id: str
        self.is_closed = is_closed
        self.innerText: str = ""
        self.Config.use_threads = use_threads
        self.Config.use_processes = use_processes
        super().__init__()

    @abstractmethod
    def validateTag(self, tag: Any) -> Any:
        pass

    @abstractmethod
    def validateAttrs(self, attrs: Any) -> Any:
        pass

    @abstractmethod
    def _set_tag(self, text: Any) -> Any:
        pass

    @classmethod
    @abstractmethod
    def _find_inner_tags(cls, text: Any) -> Any:
        pass

    # @abstractmethod
    def _set_inner_tag(self, text: str):
        child = self.__class__(text=text)
        child.parent = self
        self.addChild(child)

    @abstractmethod
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
        return repr(f"<Tag: {self.tag}>")


class ATag(ABC):
    """Base tag class."""
    __slots__ = ("tag", "innerText", 'attrs', "id", "is_closed")
    _patterns: Enum

    def __init__(self, is_closed: bool = True):
        self.tag: str = ''
        self.attrs: dict = {}
        self.id: str
        self.is_closed = is_closed
        self.innerText: str = ""
        super().__init__()

    @abstractmethod
    async def __ainit__(self, text: str):
        pass

    @abstractmethod
    async def validateTag(self, tag: Any) -> Any:
        pass

    @abstractmethod
    async def validateAttrs(self, attrs: Any) -> Any:
        pass

    @abstractmethod
    async def _set_tag(self, text: Any) -> Any:
        pass

    @classmethod
    @abstractmethod
    async def _find_inner_tags(cls, text: Any) -> Any:
        pass

    # @abstractmethod
    async def _set_inner_tag(self, text: str):
        child = self.__class__(text=text)
        child.parent = self
        self.addChild(child)

    @abstractmethod
    async def findAll(self, tag_name, **kwargs):
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
        return repr(f"<Tag: {self.tag}>")


class BaseAttribute(ABC):
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




