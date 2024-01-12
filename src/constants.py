from string import Template
import re

CHANNEL_TEMPLATE: Template = Template(
    "span[class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae"
    " le5p0ye3 l7jjieqr _11JPr'][title='$channel']"
)
FILENAME_TEMPLATE: Template = Template("$channel.csv")
SELECTORS: dict[str, str] = {
    "channels_button": "div[class='_3ndVb fbgy3m38 ft2m32mm oq31bsqd nu34rnf1']"
    "[title='Canais']",
    "channel": "span[class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 "
               "l7jjieqr _11JPr']",
    "channel_list": "div[class='_3YS_f _2A1R8'][aria-label='Lista de canais']",
    "message": "span[class='_11JPr selectable-text copyable-text']",
    "hour": "span[class='l7jjieqr fewfhwl7'][dir='auto']",
    "reactions": "button[class='dhq51u3o']",
}
WA_URL: str = "https://web.whatsapp.com/"
MINIMUM_MESSAGE_SIZE: int = 20
LONG_TIME: int = 300
SHORT_TIME: int = 10
WHITESPACE_PATTERN = re.compile(r"\s+")
SPACE_PATTERN = re.compile(r"\s")
SPLIT_PATTERN = re.compile(r"[.!]")
