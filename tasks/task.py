import csv
from time import sleep
from typing import Literal

from botasaurus import *

import src.utils as utils
from src.constants import PATH, selectors


def task(*, channel: Literal["g1", "tv_globo"], headless: bool) -> None:
    """
    Perform a series of tasks using the given browser driver and data.

    :param channel: The channel to join.
    :param headless: Whether to run in headless mode.
    """

    # noinspection PyUnusedLocal
    @browser(profile="whatsapp", headless=headless)
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

        messages = utils.get_messages(driver)
        hours = utils.get_hour(driver)
        reactions = utils.get_reactions(driver)

        print(len(messages), len(hours), len(reactions))

        if len(reactions) > len(messages):
            reactions.pop(0)
        elif len(reactions) < len(messages):
            reactions.pop(-1)

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

        with utils.secure_open_write(file_name=channel) as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    if utils.valid_channel(channel):
        main_task()
