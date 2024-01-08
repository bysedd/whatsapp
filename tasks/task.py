from time import sleep

from botasaurus import *

import src.utils as utils
from src.constants import selectors, available_channels


def task(*, channels: available_channels, headless: bool) -> None:
    """
    Perform a series of tasks using the given browser driver and data.

    :param channels: The list of channels to scraping.
    :param headless: Whether to run in headless mode.
    """
    # noinspection PyUnusedLocal
    @browser(
        headless=headless,
        profile="whatsapp",
        reuse_driver=True,
        block_images=True,
        output=None,
    )
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
        # Wait 5 minutes for WhatsApp to open completely
        driver.click(selectors["channels_button"], wait=300)
        driver.click(selectors["channels"][channel])
        sleep(10)

        messages = utils.get_messages(driver)
        hours = utils.get_hour(driver)
        reactions = utils.get_reactions(driver)

        if len(reactions) > len(messages):
            reactions.pop(0)
        if len(hours) > len(messages):
            hours.pop(0)

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

        bt.write_csv(data=data, filename=f"data_{channel}.csv")

    for channel in channels:
        if utils.valid_channel(channel):
            main_task()
