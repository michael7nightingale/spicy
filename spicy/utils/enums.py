from enum import Enum
import re


class XMLPatterns(Enum):
    INNER_TAG_PATTERN: re.Pattern = re.compile(r"(<([/\-_a-zA-Z1-6]+)[^>]*>)")
    TAG_PATTERN: re.Pattern = re.compile(r'<(?P<tag>[\w\-_]+)(?P<attrs>[^>]*)>(?P<inner_tags>.*)</\1>', re.DOTALL)
    ATTRS_PATTERN: re.Pattern = re.compile(r"(?P<name>[\-_\w]*)\s*?=\s*?(?P<comma>[\"\'])?(?P<value>[0-9a-zA-Z-:_;,./ ]*)(?P=comma)?")
    XML_PATTERN: re.Pattern = re.compile(r"<?xml\s+version=(?P<comma>[\"\'])?([\.\d]+)(?P=comma)?\?>")


class HTMLPatterns(Enum):
    ATTRS_PATTERN: re.Pattern = re.compile(r"(?P<name>[\-_\w]*)\s*?=\s*?(?P<comma>[\"\'])(?P<value>.*?)(?P=comma)")
    TAG_PATTERN: re.Pattern = re.compile(r'<(?P<tag>[\w\-_]+)(?P<attrs>[^>]*)>(?P<inner_tags>.*)</\1>', re.DOTALL)
    TAG_UNCLOSED_PATTERN: re.Pattern = re.compile(r"<(\w*)\s*(.*?)>")
    INNER_TAG_PATTERN: re.Pattern = re.compile(r"(<([/\-_a-zA-Z1-6!-]+)[^>]*>)")
    ATTRIBUTE_PATTERN: re.Pattern = re.compile(r"<(\w*)\s*(.*?)>")

