import threading
import multiprocessing as mp
from abc import abstractmethod
from typing import Type

from ..base.tag import Tag
from spicy.tree import Tree


class BaseDocument(Tree):
    """
    Base document class. Tree contains Tag-nodes
    """
    tag: str
    tagType: Type[Tag]

    class Config:
        """
        Configuration class
        """
        use_threads = False
        use_processes = False

    def __init__(self, text: str | None = None,
                 use_threads: bool = False,
                 use_processes: bool = False):
        Tree.__init__(self)  # only trick I have to do
        self.Config.use_threads = use_threads
        self.Config.use_processes = use_processes
        if text is not None:
            self._setDocument(text=text)

    def toText(self, layer: int = 0, tab: bool = True, split: str = "\n") -> str:
        """
        Returns the string object of the tag, including all children and tabs
        """
        tab = "  " if tab else ""
        text = f"<{self.tag}>{split}"
        for ch in self.children:

            text += "\n" + ch.toText(layer + 1, tab, split)
        text += f"</{self.tag}>{split}"
        return text

    def _setDocument(self, text: str) -> None:
        """
        Set document.
        """
        match_text = self.tagType._patterns.TAG_PATTERN.value.findall(text)
        tag, attrs, inner = match_text[0]
        self._validateTag(tag)  # tag validation
        del tag
        inner_tags, inner_text = self.tagType._findInnerTags(text=inner)
        self.innerText = inner_text
        # decide tasks processing type
        if self.Config.use_processes:
            with mp.Pool() as pool:
                pool.map(self._setInnerTag, inner_tags)
        elif self.Config.use_threads:
            self._setInnerTagQueue(inner_tags)
        else:
            for t in inner_tags:
                self._setInnerTag(t)

    def _setInnerTag(self, text: str) -> None:
        """
        Set sync inner tag.
        """
        inner_tag = self.tagType(
            text=text,
            use_threads=self.Config.use_threads,
            use_processes=self.Config.use_processes
        )
        inner_tag.parent = self
        self.appendChild(inner_tag)

    def _setInnerTagQueue(self, inner_tags: list):
        """
        Set inner tag, but every child must be on its place.
        Last tag in the found should be really the last one after that program continues.
        """
        n = len(inner_tags)
        n_ready = 0
        event = threading.Event()
        self.children = [None] * n

        def inner(number, text: str):
            nonlocal self, n, n_ready, event
            inner_tag = self.tagType(
                text=text,
                use_threads=self.Config.use_threads,
                use_processes=self.Config.use_processes
            )
            inner_tag.parent = self
            self.children[number] = inner_tag

            n_ready += 1
            if n_ready == n:
                event.set()

        for idx, tag in enumerate(inner_tags):
            th = threading.Thread(
                target=inner,
                args=(idx, tag)
            )
            th.start()

        while not event.wait():
            pass

    def _validateTag(self, tag: str):
        """
        Tag validation.
        """
        tag = tag.strip()
        if tag != self.tag:
            raise ValueError('HTML tag is required')

    def getElementById(self, id_: str):
        for ch in self.iterChildren():
            if ch.id == id_:
                return ch

    @abstractmethod
    def findIter(self, *args, **kwargs):
        pass

    @abstractmethod
    def findAll(self, *args, **kwargs) -> list:
        pass

    def __str__(self):
        return self.toText()


# class BaseADocument(Tree):
#     tag: str
#     tag_type: Type[ATag]
#
#     def __init__(self):
#         Tree.__init__(self)
#
#     async def __ainit__(self, text):
#         await self._set_document(text)
#
#     def to_text(self, layer: int = 0, tab: bool = True, split: str = "\n"):
#         """
#         Returns the string object of the tag, including all children and tabs
#         """
#         tab = "  " if tab else ""
#         text = f"<{self.tag}>{split}"
#         for ch in self.children:
#             text += "\n" + ch.toText(layer + 1, tab, split)
#         text += f"</{self.tag}>{split}"
#         return text
#
#     async def _set_document(self, text: str):
#         """
#         Set document.
#         """
#         match_text = self.tag_type._patterns.TAG_PATTERN.value.findall(text)
#         tag, attrs, inner = match_text[0]
#         await self._validate_tag(tag)  # tag validation
#         del tag
#         inner_tags, inner_text = await self.tag_type._find_inner_tags(text=inner)
#         self.innerText = inner_text
#         # decide tasks processing type
#         for t in inner_tags:
#             await self._set_inner_tag(t)
#             await asyncio.sleep(0)
#
#     async def _set_inner_tag(self, text: str):
#         """
#         Set sync inner tag.
#         """
#         inner_tag = self.tag_type()
#         await inner_tag.__ainit__(text)
#         inner_tag.parent = self
#         self.addChild(inner_tag)
#
#     async def _validate_tag(self, tag: str):
#         """
#         Tag validation.
#         """
#         tag = tag.strip()
#         if tag != self.tag:
#             raise ValueError('HTML tag is required')
#
#     def __str__(self):
#         return self.to_text()
