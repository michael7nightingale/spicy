import re

html_text = """
    123
    <div class="media_link__info">
    <meta charset='utf-8'>
      <a class="media_link__title" title="Первое занятие бесплатно&#33;" href="https://vk.com/itco">Первое занятие бесплатно&#33;</a>
       <a class="media_link__subtitle" title="Первое занятие бесплатно&#33;" href="https://vk.com/itco">Первое занятие бесплатно&#33;</a>
        <div>
            <p>text heello</p>
        </div>
    </div>
    <div class="media_link__buttons ">
          <a class="None" title="Первое занятие бесплатно&#33;" href="https://vk.com/itco">Первое занятие бесплатно&#33;</a>
    </div>

  """

one_ended_tags = {"meta", "link", "input"}


def find_inner_tags(text: str) -> tuple[list[str], str]:
    pattern = re.compile(r"(<([/\w]+)[^>]*>)")
    tag_stack = []
    inner_tags = []
    unclosed_tags = []
    last_inner_tag = ''
    tag = pattern.search(text)

    while tag:
        tag_beginning, tag_name = tag.groups()
        idx = text.index(tag_beginning)
        if tag_name in one_ended_tags:
            from_replace_idx = idx
            last_inner_tag += tag_beginning
            unclosed_tags.append(tag_beginning)
            text = text.replace(tag_beginning, '', 1)

        elif '/' in tag_name:
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

        tag = pattern.search(text)

    return inner_tags, text


if __name__ == '__main__':
    res = find_inner_tags(html_text)
    print(*res[0], sep='\n\n')


