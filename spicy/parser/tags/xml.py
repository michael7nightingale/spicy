import threading
import multiprocessing as mp

from spicy.parser.tags.bases import Tag
from spicy.tree import Node, Tree
from spicy.utils.enums import XMLPatterns


class XMLTag(Tag, Node):
    """XML tag class."""
    __slots__ = ("tag", "innerText", 'attrs')
    _patterns = XMLPatterns

    def __init__(self, text: str):
        super().__init__(text)
        self._set_tag(text)

    def _set_tag(self, text: str, parent=None):
        if parent is None:  # set parent after the simple call
            parent = self
        if isinstance(parent, Tree):
            version = float(self._patterns.XML_PATTERN.value.findall(text)[0][1])
            if not version:
                raise ValueError("Xml version is required.")

        match_text = self._patterns.TAG_PATTERN.value.findall(text)
        tag, attrs, inner = match_text[0]

        self.tag = self.validateTag(tag)     # tag validation
        del tag

        match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
        del attrs
        self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])

        inner_tags, inner_text = self._find_inner_tags(inner)
        self.innerText = inner_text
        # decide what task type to user
        if self.Config.use_processes:
            with mp.Pool() as pool:
                pool.map(self._set_inner_tag, inner_tags)
        elif self.Config.use_threads:
            for t in inner_tags:
                threading.Thread(target=self._set_inner_tag, args=(t,)).start()
        else:
            for t in inner_tags:
                self._set_inner_tag(text=t)

    @classmethod
    def _find_inner_tags(cls, text: str) -> tuple[list[str], str]:
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
