# Spicy
### is a tag-based parser of text. 
For example, HTML or XML are based on tags. And data text parsing can be useful when
you need to find some tags by name and attributes or take separate parts of document. 

## Running

```commandline
git clone 'https://github.com/michael7nightingale/spicy.git' 
```

Python >= 3.11
There is no any installed python libraries. Every thing is from the box.
```python
"""your parser file"""
from spicy import Spicy
from urllib.request import Request,urlopen

request = Request(url='https://example.com/')
with urlopen(request) as response:
    html_text = response.read().decode(encoding='utf-8')
    
spicy = Spicy(
    text=html_text, 
    doctype='html'    # it`s already default
)

print(spicy.tag)    # html
print(spicy.children)   # ['<Tag: head>', '<Tag: body>']
print(spicy)    # all the document in string type

head, body = spicy.children
print(el.attributes for el in body)

```


Spicy tags and document have rich searching logic: 
- `findAll()` - returns the list of tag objects with the given parameters;
- `findIter()` - generator version of `findAll()`, can reduce memory usage;
- `findFirst()` - returns first tag object with given parameters;
- `findLast()` - returns last tag object with given parameters;
- `getElementById()` - returns tag object with given id;

Useful properties:
- `tag`  - represents tag name (link, div, html, img, etc.)
- `className` - class attribute value, if exists;
- `id` - id attribute value, if exists;
- `attributes` - representation of all tag options (attributes), for example: align=center, href=/admin/user;
- `parent` - parent tag node of DOM;
- `children` - the list of children tag nodes;

