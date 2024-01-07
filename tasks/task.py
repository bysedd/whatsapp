import csv
from pathlib import Path
from time import sleep

from botasaurus import *

from src.utils import get_hour, get_messages, get_reactions, selectors

PATH = Path(__file__).parent.parent / "output"


# noinspection PyUnusedLocal
@browser(profile="whatsapp", headless=True, block_images=True)
def main_task(driver: AntiDetectDriver, data):
    """
    This method performs a series of tasks using the given browser driver and data.
    It navigates to the WhatsApp web page, join a specific channel.
    Then it retrieves messages, hours, and reactions from the web page.

    The method then processes the retrieved data and creates a list of dictionaries,
    where each dictionary contains message, hour, emojis, and total reaction count.

    Finally, it saves the processed data in a CSV file.

    :param driver: An instance of AntiDetectDriver.
    :param data: A list of data to be processed and saved.
    :return: A list of dictionaries containing processed data.
    """
    driver.organic_get("https://web.whatsapp.com/", accept_cookies=True)
    driver.click(selectors["channels_button"], wait=300)
    driver.click(selectors["channels"]["tv_globo"])
    sleep(10)

    messages = get_messages(driver)
    hours = get_hour(driver)
    reactions = get_reactions(driver)

    data = []
    for i in range(len(messages) - 1, 0, -1):
        emojis, total = reactions[i]
        data.append(
            {
                "message": messages[i],
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
