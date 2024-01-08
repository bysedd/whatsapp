import csv
from pathlib import Path
from time import sleep
from typing import Literal

from botasaurus import *

from src.utils import get_hour, get_messages, get_reactions, valid_channel
from src.constants import selectors

PATH = Path(__file__).parent.parent / "output"


def task(*, channel: Literal['g1', 'tv_globo']) -> None:
    """
    Perform a series of tasks using the given browser driver and data.

    :param channel: The channel to join.
    """
    # noinspection PyUnusedLocal
    @browser(profile="whatsapp", headless=False)
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
        driver.organic_get("https://web.whatsapp.com/")
        driver.click(selectors["channels_button"], wait=300)
        driver.click(selectors["channels"][channel])
        sleep(10)

        messages = get_messages(driver)
        hours = get_hour(driver)
        reactions = get_reactions(driver)

        data = []
        for i in range(len(messages) - 1, 0, -1):
            if len(reactions) > len(messages):
                emojis, total = reactions[i + 1]
            else:
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

        with open(PATH / f"data_{channel}.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    if valid_channel(channel):
        main_task()
