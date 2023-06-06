# Spicy (development) 
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
# your random file
from spicy import Spicy
from urllib.request import Request,urlopen

request = Request(url='https://example.com/')
with urlopen(request) as response:
    html_text = response.read().decode(encoding='utf-8')
    
spicy = Spicy(
    text=html_text, 
    type_='html'
)

print(spicy.tag)    # html
print(spicy.children)   # ['<Tag: head>', '<Tag: body>']
print(spicy)    # all the document in string type
```
