from typing import TypeVar
from spicy.tree.base import BaseNode, BaseTree


NodeVar = TypeVar('NodeVar')


class Node(BaseNode):
    """
    Node class. Secondary elements of the tree.
    """
    def findIndex(self, node: NodeVar | None = None) -> int | None:
        """Find index of the node in its parent children list is it exists."""
        if node is None:
            node = self
        if node.parent is None:
            return None

        return node.parent.children.index(node)

    def findNext(self, node: NodeVar | None = None,
                 ignore_children: bool = False) -> NodeVar | None:
        """Find the next Node in the tree"""
        if node is None:
            node = self

        if not ignore_children:     # if we want to go up the tree
            if node.children:
                return node.children[0]

        # get index of the node in parent  children`s list
        node_idx: int | None = node.findIndex()
        if node_idx is None:
            return None     # incorrect data or node is the most super

        if node_idx == len(node.parent.children) - 1:   # find in the next parent children
            return node.findNext(node.parent, True)

        else:
            return node.parent.children[node_idx + 1]

    def findParent(self):
        """Get patent"""
        return self.parent

    def findPrevious(self, node: NodeVar | None = None) -> NodeVar | None:
        """Get previous element by the top."""
        if node is None:
            node = self
        node_idx = node.findIndex(node=node)
        if node_idx is None:
            return None     # incorrect data or node is the most super

        if node_idx == 0:
            return node.parent

        return node.parent.children[node_idx + 1]

    def appendChild(self, child: NodeVar) -> None:
        """Adding new child in list"""
        if isinstance(child, Node):
            self.children.append(child)
        else:
            raise ValueError("Node child must by Node instance")


class Tree(BaseTree):
    """
    Tree class. Has no parents. Only children nodes.
    """

    def appendChild(self, child: NodeVar) -> None:
        """Adding new child in list"""
        if isinstance(child, Node):
            self.children.append(child)
        else:
            raise ValueError("Node child must by Node instance")

    def findNext(self, node: NodeVar | None = None,
                 ignore_children: bool = False) -> NodeVar | None:
        """Find the next Node in the tree"""
        if node is None:
            node = self

        if not ignore_children:     # if we want to go up the tree
            if node.children:
                return node.children[0]

        if isinstance(node, Node):
            # get index of the node in parent  children`s list
            node_idx: int | None = node.findIndex(node=node)
            if node_idx is None:
                return None     # incorrect data or node is the most super

            if node_idx == len(node.parent.children) - 1:   # find in the next parent children
                return self.findNext(node.parent, True)

            else:
                return node.parent.children[node_idx + 1]
