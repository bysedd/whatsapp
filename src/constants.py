from string import Template

CHANNEL_TEMPLATE = Template(
    "span[class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae"
    " le5p0ye3 l7jjieqr _11JPr'][title='$channel']"
)
FILENAME_TEMPLATE = Template("$channel.csv")
SELECTORS = {
    "channels_button": "div[class='_3ndVb fbgy3m38 ft2m32mm oq31bsqd nu34rnf1']"
    "[title='Canais']",
    "channels": {
        "tv_globo": CHANNEL_TEMPLATE.substitute(channel="TV Globo"),
        "g1": CHANNEL_TEMPLATE.substitute(channel="g1"),
        "globo_com": CHANNEL_TEMPLATE.substitute(
            channel="globo.com I Últimas notícias: "
                    "jornalismo, esporte e entretenimento"
        )
    },
    "message": "span[class='_11JPr selectable-text copyable-text']",
    "hour": "span[class='l7jjieqr fewfhwl7'][dir='auto']",
    "reactions": "button[class='dhq51u3o']",
}
AVAILABLE_CHANNELS = list(SELECTORS["channels"].keys())
WA_URL = "https://web.whatsapp.com/"
WAIT_TIME = 300
SLEEP_TIME = 10
