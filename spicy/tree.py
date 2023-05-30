"""
Both-sides linked trees.
"""
import abc
from typing import Any


class NodeBase(abc.ABC):
    def __init__(self,
                 data=None,
                 parent=None,
                 children=None):
        self.data: Any = data
        self.parent: Node = parent
        if children is not None:
            self.children: list[Node] = list(children)
        else:
            self.children = []

    @abc.abstractmethod
    def findNext(self, node, ignore_children: bool = True):
        pass

    @abc.abstractmethod
    def findIndex(self, node) -> int | None:
        pass

    @abc.abstractmethod
    def findPrevious(self, node) -> int | None:
        pass

    def __iter__(self):
        pass


class Node(NodeBase):

    def findIndex(self, node: NodeBase | None = None) -> int | None:
        """Find index of the node in its parent children list is it exists."""
        if node is None:
            node = self
        if node.parent is None:
            return None

        return node.parent.children.index(node)

    def findNext(self, node: NodeBase | None = None,
                 ignore_children: bool = False) -> NodeBase | None:
        """Find the next Node in the tree"""
        if node is None:
            node = self

        if not ignore_children:     # if we want to go up the tree
            if node.children:
                return node.children[0]

        # get index of the node in parent  children`s list
        node_idx: int | None = self.findIndex(node=node)

        if node_idx is None:
            return None     # incorrect data or node is the most super

        if node_idx == len(node.parent.children):   # find in the next parent children
            return self.findNext(node.parent, True)

        else:
            return node.parent.children[node_idx + 1]

    def findParent(self):
        """Get patent"""
        return self.parent

    # def findParents(self, node:  NodeBase | None = None):
    #     """Find all super nodes of the node"""
    #     if node is None:
    #         node = self
    #     parents = []
    #     now_parent = node.parent
    #     while now_parent is not None:
    #         to_extend = []
    #         for child in now_parent[:node.findIndex()]:
    #             for
    #
    #     return parents

    def findPrevious(self, node: NodeBase | None = None) -> NodeBase | None:
        """Get previous element by the top."""
        if node is None:
            node = self
        node_idx = node.findIndex(node=node)
        if node_idx is None:
            return None     # incorrect data or node is the most super

        if node_idx == 0:
            return node.parent

        return node.parent.children[node_idx + 1]

    def addChild(self, child: NodeBase) -> None:
        """Adding new child in list"""
        if isinstance(child, NodeBase):
            self.children.append(child)

        raise ValueError("Node child must by Node instance")


class Tree:

    def __init__(self,
                 data: Any,
                 root: Node | None = None):
        self.root = root
        self.root_data = data

    @classmethod
    def add(cls, parent: Node, *nodes):
        if parent is None:
            raise ValueError("Parent is None~")

        for node in nodes:
            parent.children.append(node)


if __name__ == '__main__':
    n_root = Node(data=123)

    tree = Tree(data=0, root=n_root)

    tree.add(n_root, Node(10, n_root), Node(12003, n_root))

    last = n_root.children[-1]
    print([i.data for i in last.findParents()])
