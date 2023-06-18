import asyncio
import threading
import multiprocessing as mp

from spicy.parser.tags.bases import Tag, ATag
from spicy.tree import Node, Tree
from spicy.utils.enums import HTMLPatterns


attributes_classes: set[str] = {
    "meta", "link", "img",
    "path", "base", "hr",
    "input", "br",

}


class HTMLTag(Tag, Node):
    """HTML tag class."""
    __slots__ = ("class_", "style", "tag", "innerText", 'attrs', "id", "is_closed")
    _patterns = HTMLPatterns

    def __init__(self, text: str,
                 use_threads: bool = False,
                 use_processes: bool = False):
        super().__init__(
            text,
            use_threads=use_threads,
            use_processes=use_processes
        )
        self.class_: str
        self.style: str
        self._set_tag(text=text)

    def validateTag(self, tag: str):
        if tag:
            return tag
        else:
            raise ValueError("Tag is not valid! (it is empty)")

    @classmethod
    def _find_inner_tags(cls, text: str) -> tuple[list[str], str]:
        tag_stack = []
        inner_tags = []
        unclosed_tags = []
        last_inner_tag = ''
        tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)

        while tag:
            tag_beginning, tag_name = tag.groups()
            idx = tag.start()
            if '--' in tag_name:
                text = text.replace(tag_beginning, '', 1)

            elif tag_name in attributes_classes:
                last_inner_tag += tag_beginning
                unclosed_tags.append(tag_beginning)
                text = text.replace(tag_beginning, '', 1)

            elif '/' in tag_name:
                last_inner_tag += text[from_replace_idx:idx + len(tag_beginning)]
                text = text[:from_replace_idx] + text[idx + len(tag_beginning):]
                last_stack_tag = tag_stack[-1]
                if '--' in tag_name:
                    if '!--' in last_stack_tag and last_stack_tag.replace('!--', '') == tag_name.replace('--', '').lstrip('/'):
                        tag_stack.pop()
                else:
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

    def validateAttrs(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except:
            raise AttributeError("Attributes are not valid")

    def _set_tag(self, text):
        FILL_UNSTATED_WITH = None

        # if parent is None:  # set parent after the simple call
        #     parent = self

        try:
            match_text = self._patterns.TAG_PATTERN.value.findall(text)
            tag, attrs, inner = match_text[0]
            self.tag = self.validateTag(tag)     # tag validation
            del tag

            match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
            del attrs
            self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
            self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
            self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)

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
        except (IndexError, ):
            ATTRIBUTE_PATTERN = self._patterns.ATTRIBUTE_PATTERN
            match_text = ATTRIBUTE_PATTERN.value.findall(text)
            tag, attrs = match_text[0]
            self.tag = tag
            self.is_closed = False
            match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
            del attrs

            self.attrs = self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
            self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
            self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)

    def findAll(self, tag_name, **kwargs):
        for t in self:
            if t.tag == tag_name:
                if not kwargs:
                    yield t
                else:
                    if 'class_' in kwargs:
                        kwargs['class'] = kwargs['class_']
                        del kwargs['class_']
                    if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
                        yield t


class AHTMLTag(ATag, Node):
    """HTML tag class."""
    __slots__ = ("class_", "style", "tag", "innerText", 'attrs', "id", "is_closed")
    _patterns = HTMLPatterns

    def __init__(self):
        super().__init__()
        self.class_: str
        self.style: str

    async def __ainit__(self, text: str):
        await self._set_tag(text)

    async def validateTag(self, tag: str):
        if tag:
            return tag
        else:
            raise ValueError("Tag is not valid! (it is empty)")

    @classmethod
    async def _find_inner_tags(cls, text: str) -> tuple[list[str], str]:
        tag_stack = []
        inner_tags = []
        unclosed_tags = []
        last_inner_tag = ''
        tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)

        while tag:
            tag_beginning, tag_name = tag.groups()
            idx = text.index(tag_beginning)

            if tag_name in attributes_classes:
                last_inner_tag += tag_beginning
                unclosed_tags.append(tag_beginning)
                text = text.replace(tag_beginning, '', 1)

            elif '/' in tag_name:
                last_inner_tag += text[from_replace_idx:idx + len(tag_beginning)]
                text = text[:from_replace_idx] + text[idx + len(tag_beginning):]
                last_stack_tag = tag_stack[-1]
                if '--' in tag_name:
                    if '!--' in last_stack_tag and last_stack_tag.replace('!--', '') == tag_name.replace('--', '').lstrip('/'):
                        tag_stack.pop()
                else:
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

    async def validateAttrs(self, attrs: list[tuple]):
        try:
            return dict(attrs)
        except:
            raise AttributeError("Attributes are not valid")

    async def _set_tag(self, text):
        FILL_UNSTATED_WITH = None

        # if parent is None:  # set parent after the simple call
        #     parent = self

        if text.count('<') > 1:
            match_text = self._patterns.TAG_PATTERN.value.findall(text)
            tag, attrs, inner = match_text[0]
            self.tag = await self.validateTag(tag)     # tag validation
            del tag

            match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
            del attrs
            self.attrs = await self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
            self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
            self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)

            inner_tags, inner_text = await self._find_inner_tags(inner)
            self.innerText = inner_text

            # decide what task type to user
            for t in inner_tags:
                await self._set_tag(t)
                await asyncio.sleep(0)

        else:
            ATTRIBUTE_PATTERN = self._patterns.ATTRIBUTE_PATTERN
            match_text = ATTRIBUTE_PATTERN.value.findall(text)
            tag, attrs = match_text[0]
            self.tag = tag
            self.is_closed = False
            match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
            del attrs

            self.attrs = await self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
            self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
            self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)

    async def findAll(self, tag_name, **kwargs):
        for t in self:
            if t.tag == tag_name:
                if not kwargs:
                    yield t
                else:
                    if 'class_' in kwargs:
                        kwargs['class'] = kwargs['class_']
                        del kwargs['class_']
                    if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
                        yield t


