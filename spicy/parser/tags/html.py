import threading
import multiprocessing as mp

from spicy.parser.tags.bases import Tag
from spicy.tree import Node
from spicy.utils.enums import HTMLPatterns


UNCLOSED_TAG: set[str] = {
    "meta", "link", "img",
    "path", "base", "hr",
    "input", "br",

}


class HTMLTag(Tag, Node):
    """HTML tag class."""
    __slots__ = ("className", "style", "tag", "innerText", 'attributes', "id", "isClosed")
    _patterns = HTMLPatterns

    def __init__(self,
                 tag: str | None = None,
                 text: str | None = None,
                 isClosed: bool = True,
                 use_threads: bool = False,
                 use_processes: bool = False):
        super().__init__(
            text,
            use_threads=use_threads,
            use_processes=use_processes
        )
        if text is not None:
            if tag is not None:
                raise ValueError("Either text or tag is required.")
            self._setTag(text=text)
        else:
            if tag is None:
                raise ValueError("Either text or tag is required.")
            self.tag = tag
        self.className: str | None = None
        self.isClosed = isClosed

    def validateTag(self, tag: str):
        """
        Tag validation.
        """
        if tag:
            return tag
        else:
            raise ValueError("Tag is not valid! (it is empty)")

    @classmethod
    def _findInnerTags(cls, text: str) -> tuple[list[str], str]:
        """
        Find inner tags in text.
        """
        tag_stack = []
        inner_tags = []
        unclosed_tags = []
        last_inner_tag = ''
        from_replace_idx: int = 0
        tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)
        while tag:
            tag_beginning, tag_name = tag.groups()
            idx = tag.start()
            if '--' in tag_name:
                text = text.replace(tag_beginning, '', 1)

            elif tag_name in UNCLOSED_TAG:
                last_inner_tag += tag_beginning
                unclosed_tags.append(tag_beginning)
                text = text.replace(tag_beginning, '', 1)

            elif '/' in tag_name:
                last_inner_tag += text[from_replace_idx:idx + len(tag_beginning)]
                text = text[:from_replace_idx] + text[idx + len(tag_beginning):]
                last_stack_tag = tag_stack[-1]
                if '--' in tag_name:
                    if '!--' in last_stack_tag and last_stack_tag.replace('!--', '') == tag_name.replace('--',
                                                                                                         '').lstrip(
                            '/'):
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

    def validateAttributes(self, attrs: list[tuple]):
        """
        Attributes validation.
        """
        try:
            return dict(attrs)
        except Exception:
            raise AttributeError("Attributes are not valid")

    def _setTag(self, text):
        """
        Set tag.
        """
        FILL_UNSTATED_WITH = None
        try:
            match_text = self._patterns.TAG_PATTERN.value.findall(text)
            tag, attributes, inner = match_text[0]
            self.tag = self.validateTag(tag)  # tag validation
            del tag
            match_attributes = self._patterns.ATTRS_PATTERN.value.findall(attributes)
            del attributes
            self.attributes = self.validateAttributes([i[:1] + i[2:] for i in match_attributes])
            self.id = self.attributes.get('id', FILL_UNSTATED_WITH)
            self.className = self.attributes.get('class', FILL_UNSTATED_WITH)
            inner_tags, innerText = self._findInnerTags(inner)
            self.innerText = innerText
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

        except (IndexError, ):
            ATTRIBUTE_PATTERN = self._patterns.ATTRIBUTE_PATTERN
            match_text = ATTRIBUTE_PATTERN.value.findall(text)
            tag, attributes = match_text[0]
            self.tag = tag
            self.isClosed = True
            match_attributes = self._patterns.ATTRS_PATTERN.value.findall(attributes)
            del attributes
            self.attributes = self.validateAttributes([i[:1] + i[2:] for i in match_attributes])
            self.id = self.attributes.get('id', FILL_UNSTATED_WITH)
            self.className = self.attributes.get('class', FILL_UNSTATED_WITH)

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
            inner_tag = self.__class__(
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

    def findAll(self, tag_name, **kwargs):
        """
        Find tags on set parameters.
        """
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

    def toText(self, layer: int = 0, tab: bool = True, split: str = "\n"):
        attributes = " ".join((f"{name}='{val}'" for name, val in self.attributes.items()))
        tab = "  " if tab else ""
        if self.isClosed:
            to_cont = split if self.children else ""
            text = tab * layer + f"<{self.tag} {attributes}>{self.innerText}{to_cont}"
        else:
            text = tab * layer + f"<{self.tag} {attributes}>{split}"
        for ch in self.children:
            text += ch.toText(layer + 1, tab, split)
        if self.isClosed:
            text += tab * layer + f"</{self.tag}>{split}"
        return text


# class AHTMLTag(ATag, Node):
#     """
#     HTML tag class.
#     """
#     __slots__ = ("class_", "style", "tag", "innerText", 'attrs', "id", "is_closed")
#     _patterns = HTMLPatterns
#
#     def __init__(self,
#                  use_threads: bool = False,
#                  use_processes: bool = False):
#         super().__init__(
#             use_threads=use_threads,
#             use_processes=use_processes
#         )
#         self.class_: str
#         self.style: str
#
#     async def __ainit__(self, text: str):
#         """
#         Костыль для асинхронности
#         """
#         await self._set_tag(text)
#
#     async def validateTag(self, tag: str):
#         """
#         Tag validation.
#         """
#         if tag:
#             return tag
#         else:
#             raise ValueError("Tag is not valid! (it is empty)")
#
#     @classmethod
#     async def _find_inner_tags(cls, text: str) -> tuple[list[str], str]:
#         """
#         Find inner tags in text.
#         """
#         tag_stack = []
#         inner_tags = []
#         unclosed_tags = []
#         last_inner_tag = ''
#         tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)
#         while tag:
#             tag_beginning, tag_name = tag.groups()
#             idx = tag.start()
#             if '--' in tag_name:
#                 text = text.replace(tag_beginning, '', 1)
#
#             elif tag_name in UNCLOSED_TAG:
#                 last_inner_tag += tag_beginning
#                 unclosed_tags.append(tag_beginning)
#                 text = text.replace(tag_beginning, '', 1)
#
#             elif '/' in tag_name:
#                 last_inner_tag += text[from_replace_idx:idx + len(tag_beginning)]
#                 text = text[:from_replace_idx] + text[idx + len(tag_beginning):]
#                 last_stack_tag = tag_stack[-1]
#                 if '--' in tag_name:
#                     if '!--' in last_stack_tag and last_stack_tag.replace('!--', '') == tag_name.replace('--',
#                                                                                                          '').lstrip(
#                             '/'):
#                         tag_stack.pop()
#                 else:
#                     if tag_name.replace('/', '') == last_stack_tag:
#                         tag_stack.pop()
#             else:
#                 from_replace_idx = idx
#                 last_inner_tag += tag_beginning
#                 text = text.replace(tag_beginning, '', 1)
#                 tag_stack.append(tag_name)
#
#             if not tag_stack:
#                 inner_tags.append(last_inner_tag)
#                 last_inner_tag = ''
#
#             tag = cls._patterns.INNER_TAG_PATTERN.value.search(text)
#
#         return inner_tags, text.strip()
#
#     async def validateAttrs(self, attrs: list[tuple]):
#         """
#         Attributes validation.
#         """
#         try:
#             return dict(attrs)
#         except:
#             raise AttributeError("Attributes are not valid")
#
#     async def _set_tag(self, text):
#         """
#         Set tag.
#         """
#         FILL_UNSTATED_WITH = None
#         if text.count('<') > 1:
#             match_text = self._patterns.TAG_PATTERN.value.findall(text)
#             tag, attrs, inner = match_text[0]
#             self.tag = await self.validateTag(tag)  # tag validation
#             del tag
#             match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
#             del attrs
#             self.attrs = await self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
#             self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
#             self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)
#             inner_tags, inner_text = await self._find_inner_tags(inner)
#             self.innerText = inner_text
#             # decide what task type to user
#             for t in inner_tags:
#                 await self._set_tag(t)
#                 await asyncio.sleep(0)
#         else:
#             ATTRIBUTE_PATTERN = self._patterns.ATTRIBUTE_PATTERN
#             match_text = ATTRIBUTE_PATTERN.value.findall(text)
#             tag, attrs = match_text[0]
#             self.tag = tag
#             self.is_closed = False
#             match_attrs = self._patterns.ATTRS_PATTERN.value.findall(attrs)
#             del attrs
#             self.attrs = await self.validateAttrs([i[:1] + i[2:] for i in match_attrs])
#             self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
#             self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)
#
#     async def findAll(self, tag_name, **kwargs):
#         """
#         Find tags on set parameters.
#         """
#         for t in self:
#             if t.tag == tag_name:
#                 if not kwargs:
#                     yield t
#                 else:
#                     if 'class_' in kwargs:
#                         kwargs['class'] = kwargs['class_']
#                         del kwargs['class_']
#                     if all(t.attrs.get(i) == kwargs[i] for i in kwargs):
#                         yield t
