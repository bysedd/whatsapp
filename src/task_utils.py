import re
from abc import ABC, abstractmethod

from botasaurus import AntiDetectDriver

import src.constants as const
import src.utils as utils


class AbstractExtractor(ABC):
    """AbstractExtractor is an abstract base class for extractors."""

    pattern = ""

    def __init__(self, driver: AntiDetectDriver):
        self.driver = driver

    @abstractmethod
    def extract(self, list_msgs: list):
        """
        Extracts data from the given source.

        This method is used to extract data from a specific source
        and process it further.
        """

    def get_elements(self, selector: str) -> list:
        """
        Returns a list of elements found by the given selector.

        :param selector: The CSS selector to locate the elements.
        :return: A list of elements found by the given selector.
        """
        return utils.extract_list(
            self.driver.get_elements_or_none_by_selector(selector)
        )


class MessageExtractor(AbstractExtractor):
    """
    This class, `MessageExtractor`, is a subclass of `AbstractExtractor` and is
    responsible for extracting messages from a source.
    """

    pattern = r"[.!?;-|]"

    def extract(self, list_msgs: list) -> list[str]:
        """
        Extracts messages from raw messages by removing URLs and splitting them based
        on a pattern.

        :param list_msgs: A list of unformulated messages
        :return: A list of extracted messages.
        """
        new_messages = []
        for message in list_msgs:
            # Remove URLs
            message = re.sub(r"https?://.*[^s]*", "", message)
            # Remove colons
            message = re.sub(r":", "", message)
            parts = re.split(self.pattern, message)
            new_message = (
                parts[0] + parts[1]
                if len(parts[0]) < const.MINIMUM_MESSAGE_SIZE and len(parts) > 1
                else parts[0]
            )
            new_messages.append(new_message.strip())
        return new_messages


class HourExtractor(AbstractExtractor):
    """A class that extracts hours from a given input string."""

    pattern = re.compile(r"\d{2}:\d{2}")

    def extract(self, list_msgs: list) -> list[str]:
        """
        Extracts the hours from the elements and filters out duplicate hours.

        :param list_msgs: A list of unformulated messages
        :return: A list of filtered hours.
        """
        times = re.findall(self.pattern, " ".join(list_msgs))
        return times


class ReactionExtractor:
    """
    The ReactionExtractor class provides methods to extract reactions from a web page.
    """

    pattern = re.compile(r"[\d.,]+")

    def extract(self, driver: AntiDetectDriver) -> list[tuple[list, int]]:
        """
        Extracts reactions from a web page and returns a list of tuples.

        :param driver: The web driver.
        :return: A list of tuples containing emojis and the corresponding total.
        """
        raw_reactions = driver.get_elements_or_none_by_selector(
            const.SELECTORS["reactions"]
        )
        raw_reactions_texts = [
            element.get_attribute("aria-label") for element in raw_reactions
        ]
        emojis = [
            [
                emoji.get_attribute("alt")
                for emoji in element.find_elements(by="tag name", value="img")
            ]
            for element in raw_reactions
        ]
        results = []
        for i, text in enumerate(raw_reactions_texts):
            numbers = self.pattern.findall(text)
            numbers = [number.replace(".", "") for number in numbers]
            total = int(numbers[-1]) if numbers else 0
            results.append((emojis[i], total))
        return results


class ChannelExtractor:
    """This class is used to extract channels from a channel list."""

    @staticmethod
    def extract(driver: AntiDetectDriver):
        """
        Extracts the channel information from the web page.

        :param driver: The web driver.
        :return: A dictionary containing the channel name and the channel template.
        """
        channel_list = driver.get_element_or_none_by_selector(
            const.SELECTORS["channel_list"], wait=const.LONG_TIME
        )
        channels = channel_list.find_elements(
            "css selector", const.SELECTORS["channel"]
        )
        return {
            utils.simplify_channel_name(
                channel.get_attribute("title")
            ): const.CHANNEL_TEMPLATE.substitute(channel=channel.get_attribute("title"))
            for channel in channels
        }
