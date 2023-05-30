import abc
import re
from tree import Tree, Node


class HTMLElementBase(abc.ABC):
    __slots__ = ("tag", "innerText", "class_", "id", "children", "context", 'attrs')
    tag_pattern: re.Pattern
    attrs_pattern: re.Pattern

    def __init__(self, text: str) -> None:
        self.content: str = text
        self.tag: str
        self.attrs: dict
        self.class_: str
        self.id: str
        self.children: list
        self.innerText: str

        self._set_attributes(self.content)

        super().__init__()


class Attributable(abc.ABC):

    @abc.abstractmethod
    def _set_attributes(self, text: str):
        pass


class ContentMixin:
    content: str

    def __repr__(self):
        return self.content


class HTMLElementUnclosed:
    pass


class InitialMixin:
    def __init__(self):
        super().__init__()


class HTMLElement(HTMLElementBase, Node, ContentMixin):
    attrs_pattern = re.compile(r"(?P<name>\w*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[\w\s]*)(?P=comma)?")
    tag_pattern = re.compile(r"<(?P<tag>\w*)(?P<attrs>.*)>(?P<inner>[\s\S]*)</(?P=tag)>")

    def _set_attributes(self,  text: str, parent=None):
        if parent is None:
            parent = self

        FILL_UNSTATED_WITH = None

        match_text = self.tag_pattern.findall(text)
        print(match_text)
        tag, attrs, inner = match_text[0]
        # print(tag, attrs, inner)

        stripped_tag = tag.strip()
        if not stripped_tag:
            raise ValueError("Tag is not correct")
        self.tag = stripped_tag
        del tag, stripped_tag

        match_attrs = self.attrs_pattern.findall(attrs)

        self.attrs = dict((a[:1] + a[2:] for a in match_attrs))
        self.id = self.attrs.get('id', FILL_UNSTATED_WITH)
        self.class_ = self.attrs.get('class', FILL_UNSTATED_WITH)


        #
        # inner_tags = self.tag_pattern.findall(inner)
        # print(inner_tags[0][1], sep='\n')



class HTMLTree(HTMLElementBase, Tree, ContentMixin):
    pass




class MetaData:
    def __init__(self, **attrs):
        self.attrs = dict(**attrs)

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __getitem__(self, item):
        return self.attrs[item]


with open('d:/Progs/PycharmProjects/RepoFastAPI/public/templates/main/layout.html') as file:
    docs = file.read()

docs = """
       <a aria-expanded="false" role="button" data-toggle="dropdown" class="dropdown-toggle" href="#">
       Help
       <span class="caret">
       </span>
       </a>
          """

el = HTMLElement(docs)
# print(el.attrs)

