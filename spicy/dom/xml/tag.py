import threading
import multiprocessing as mp

from ..base.tag import Tag
from spicy.tree import Node, Tree
from .enum_ import XMLPatterns
from ...utils import exceptions


class XMLTag(Tag, Node):
    """XML tag class."""
    __slots__ = ("tag", "innerText", 'attrs')
    _patterns = XMLPatterns

    def __init__(self,
                 tag: str | None = None,
                 text: str | None = None,
                 use_threads: bool = False,
                 use_processes: bool = False):
        if text is not None:
            if tag is not None:
                raise exceptions.InitTagError
            self._setTag(text=text)
        else:
            if tag is None:
                raise exceptions.InitTagError
            self.tag = tag
        self.attributes: dict = {}
        self.id: str | None = None
        self.innerText: str = ""
        self.Config.use_threads = use_threads
        self.Config.use_processes = use_processes
        super().__init__()

    def _setTag(self, text: str, parent=None):
        if parent is None:  # set parent after the simple call
            parent = self
        if isinstance(parent, Tree):
            version = float(self._patterns.XML_PATTERN.value.findall(text)[0][1])
            if not version:
                raise ValueError("Xml version is required.")

        match_text = self._patterns.TAG_PATTERN.value.findall(text)
        tag, attributes, inner = match_text[0]

        self.tag = self.validateTag(tag)     # tag validation
        del tag

        match_attributes = self._patterns.ATTRS_PATTERN.value.findall(attributes)
        del attributes
        self.attributes = self.validateAttributes([i[:1] + i[2:] for i in match_attributes])

        inner_tags, inner_text = self._findInnerTags(inner)
        self.innerText = inner_text
        # decide what task type to user
        if self.Config.use_processes:
            with mp.Pool() as pool:
                pool.map(self._setInnerTag, inner_tags)
        elif self.Config.use_threads:
            for t in inner_tags:
                threading.Thread(target=self._setInnerTag, args=(t,)).start()
        else:
            for t in inner_tags:
                self._setInnerTag(text=t)

    @classmethod
    def _findInnerTags(cls, text: str) -> tuple[list[str], str]:
        tag_stack = []
        inner_tags = []
        last_inner_tag = ''
        tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)
        from_replace_idx: int = 0
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

            tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)
        return inner_tags, text.strip()

    def validateTag(self, tag: str):
        if tag:
            return tag
        else:
            raise ValueError("Tag is not valid! (it is empty)")

    def validateAttributes(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except Exception:
            raise AttributeError("Attributes are not valid")

    def findAll(self, tag_name, **kwargs):
        for t in self:
            if t.tag == tag_name:
                if not kwargs:
                    yield t
                else:
                    if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
                        yield t

    def toText(self, layer: int = 0, tab: bool = True, split: str = "\n"):
        pass
