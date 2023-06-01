import re
from typing import Any

from bases import Tag
from tree import Node, Tree


class XMLTag(Tag, Node):
    """XML tag class."""

    def _set_tag(self, text: str):
        pass

    def _find_inner_tags(self, text: Any) -> Any:
        pass

    def validateTag(self, tag: str) -> Any:
        pass

    def validateAttrs(self, attrs: Any) -> Any:
        pass
