from time import sleep

from botasaurus import *

import src.utils as utils
import src.constants as const


def main_task(*, channels: const.AVAILABLE_CHANNELS, headless: bool) -> None:
    """
    Perform a series of tasks using the given browser driver and data.

    :param channels: The list of channels to scraping.
    :param headless: Whether to run in headless mode.
    """
    # noinspection PyUnusedLocal
    @browser(
        headless=headless,
        profile="whatsapp",
        block_images=True,
        output=None,
    )
    def wrapper(driver: AntiDetectDriver, data):
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
        driver.get(const.WA_URL)
        # Wait 5 minutes for WhatsApp to open completely
        driver.click(const.SELECTORS["channels_button"], wait=const.WAIT_TIME)
        for channel in channels:
            if utils.valid_channel(channel):
                driver.click(const.SELECTORS["channels"][channel])
                sleep(const.SLEEP_TIME)

                messages = utils.get_messages(driver)
                hours = utils.get_hour(driver)
                reactions = utils.get_reactions(driver)

                messages, hours, reactions = utils.align_elements(
                    messages, hours, reactions
                )

                data = []
                for i in range(len(messages) - 1, 0, -1):
                    emojis, total = reactions[i]

                    # Pad emojis with None if its length is less than 4
                    emojis = (emojis + [None] * 4)[:4]

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

                bt.write_csv(
                    data, filename=const.FILENAME_TEMPLATE.substitute(channel=channel)
                )

    wrapper()
