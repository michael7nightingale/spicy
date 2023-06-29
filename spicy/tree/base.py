"""
Both-sides linked trees.
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar


Node = TypeVar('Node')


class BaseNode(ABC):
    """
    Base Node class
    """
    def __init__(self,
                 data: Node | None = None,
                 parent: Node | None = None,
                 children: list[Node] | None = None):
        self.children: list[Node]
        self.data: Any = data
        self.parent: Node | None = parent
        if children is not None:
            self.children = list(children)
        else:
            self.children = []

    @abstractmethod
    def findNext(self, node: Node | None = None,
                 ignore_children: bool = True):
        pass

    @abstractmethod
    def findIndex(self, node: Node | None = None) -> int | None:
        pass

    @abstractmethod
    def findPrevious(self, node: Node | None = None) -> int | None:
        pass

    def __iter__(self):
        now = self
        while now is not None:
            yield now
            now = now.findNext()

    def __len__(self):
        length = 1
        for ch in self.children:
            length += len(ch)
        return length


class BaseTree(ABC):
    """
    Base Tree class.
    """
    def __init__(self,
                 data: Any = None,
                 children: list[Node] | None = None):
        self.children: list[Node]
        self.data: Any | None = data
        if children is not None:
            self.children = list(children)
        else:
            self.children = []

    @abstractmethod
    def findNext(self, node, ignore_children: bool = True):
        pass

    def __iter__(self):
        now = self
        while now is not None:
            yield now
            now = now.findNext()

    def __len__(self):
        length = 1
        for ch in self.children:
            length += len(ch)
        return length
