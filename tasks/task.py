from botasaurus import *
from src.utils import *
from time import sleep
import csv
from pathlib import Path

PATH = Path(__file__).parent.parent / "output"


# noinspection PyUnusedLocal
@browser(profile="whatsapp", headless=True, block_images=True)
def main_task(driver: AntiDetectDriver, data):
    driver.organic_get("https://web.whatsapp.com/", accept_cookies=True)
    driver.click(selectors["channels_button"], wait=300)
    driver.click(selectors["channels"]["tv_globo"])
    sleep(10)

    messages = get_content(driver)
    hours = get_hour(driver)
    reactions = get_reactions(driver)

    data = []
    for i in range(len(messages) - 1, 0, -1):
        emojis, total = reactions[i]
        data.append(
            {
                "text": messages[i],
                "hour": hours[i],
                "emoji_1": emojis[0],
                "emoji_2": emojis[1],
                "emoji_3": emojis[2],
                "emoji_4": emojis[3],
                "total": total,
            }
        )

    with open(PATH / "data.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return data
