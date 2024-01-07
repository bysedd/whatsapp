from string import Template

channel_template = Template(
    "span[class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr'][title='$channel']"
)

selectors = {
    "channels_button": "div[class='_3ndVb fbgy3m38 ft2m32mm oq31bsqd nu34rnf1'][title='Canais']",
    "channels": {
        "tv_globo": channel_template.substitute(channel="TV Globo"),
        "g1": channel_template.substitute(channel="g1"),
    },
    "message_content": "span[class='_11JPr selectable-text copyable-text']",
    "hour_message": "span[class='l7jjieqr fewfhwl7'][dir='auto']"
}


def extract_list(list_elements: list) -> list:
    """
    :param list_elements: A list of web elements to extract text from
    :return: A list of extracted texts
    """
    return [element.text.strip() for element in list_elements]