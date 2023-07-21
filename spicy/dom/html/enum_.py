import re
from enum import Enum


class HTMLPatterns(Enum):
    ATTRS_PATTERN: re.Pattern = re.compile(r"\s*(?P<name>.*?)\s*=\s*(?P<comma>[\"\'])(?P<value>.*?)(?P=comma)")
    TAG_PATTERN: re.Pattern = re.compile(r'<(?P<tag>[\w\-_]+)(?P<attrs>[^>]*)>(?P<inner_tags>.*)</\1>', re.DOTALL)
    TAG_UNCLOSED_PATTERN: re.Pattern = re.compile(r"<(\w*)\s*(.*?)>")
    INNER_TAG_PATTERN: re.Pattern = re.compile(r"(<([/\-_a-zA-Z1-6!-]+)[^>]*>)")
    ATTRIBUTE_PATTERN: re.Pattern = re.compile(r"<(\w*)\s*(.*?)>")
