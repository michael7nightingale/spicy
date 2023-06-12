from abc import ABC, abstractmethod
from typing import Type

from spicy.parser.tags.bases import Tag
from spicy.tree import Tree


class BaseDocument(Tree):
    tag: str
    tag_type: Tag

    def __init__(self, text: str):
        Tree.__init__(self)
        self._set_document(text)

    def to_text(self, layer: int = 0, tab: bool = True, split: str = "\n"):
        """Returns the string object of the tag, incuding all children and tabs"""
        # print(self.children)
        tab = "  " if tab else ""
        text = f"<{self.tag}>{split}"
        for ch in self.children:

            text += "\n" + ch.toText(layer + 1, tab, split)
        text += f"</{self.tag}>{split}"
        return text

    def _set_document(self, text):
        match_text = self.tag_type._patterns.TAG_PATTERN.value.findall(text)
        tag, attrs, inner = match_text[0]
        self.tag = self._validate_tag(tag)  # tag validation
        del tag
        inner_tags, inner_text = self.tag_type._find_inner_tags(inner)
        self.innerText = inner_text
        for t in inner_tags:
            child = self.tag_type(t)
            child.parent = self
            self.addChild(child)

    def _validate_tag(self, tag: str):
        tag = tag.strip()
        if tag != self.tag:
            raise ValueError('HTML tag is required')

    def __str__(self):
        return self.to_text()


