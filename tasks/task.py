from time import sleep

from botasaurus import *

import tasks.task_utils as t_utils
from src import constants as const
from src import utils


def main_task(*, headless: bool) -> None:
    """
    Perform a series of tasks using the given browser driver and data.

    :param headless: Whether to run in headless mode.
    """

    # noinspection PyUnusedLocal
    @browser(
        headless=headless,
        profile="whatsapp",
        output=None,
        reuse_driver=True,
        block_images=True,
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

        channel_extractor = t_utils.ChannelExtractor(driver)
        message_extractor = t_utils.MessageExtractor(driver)
        hour_extractor = t_utils.HourExtractor(driver)
        reaction_extractor = t_utils.ReactionExtractor(driver)

        # Wait 5 minutes for WhatsApp to open completely
        driver.click(const.SELECTORS["channels_button"], wait=const.LONG_TIME)
        channels = channel_extractor.extract()

        for name, element in channels.items():
            channel_chat = driver.get_element_or_none_by_selector(
                element, wait=const.LONG_TIME
            )
            if channel_chat:
                driver.click(element)
                sleep(const.SHORT_TIME)

                messages = message_extractor.extract()
                hours = hour_extractor.extract()
                reactions = reaction_extractor.extract()

                messages, hours, reactions = utils.align_message_data(
                    messages, hours, reactions
                )

                # Create dataset with the obtained data
                data = [
                    utils.extract_data_to_dict(message, hour, reaction)
                    for message, hour, reaction in zip(messages, hours, reactions)
                ]

                bt.write_csv(
                    data[::-1],
                    filename=const.FILENAME_TEMPLATE.substitute(channel=name),
                )

                driver.refresh()
                driver.click(const.SELECTORS["channels_button"], wait=const.LONG_TIME)

    wrapper()
