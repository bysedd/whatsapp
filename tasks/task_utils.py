import re
from botasaurus import AntiDetectDriver
import src.constants as const
import src.utils as utils
from abc import ABC, abstractmethod


class AbstractExtractor(ABC):
    """AbstractExtractor is an abstract base class for extractors."""
    pattern = ''

    def __init__(self, driver: AntiDetectDriver):
        self.driver = driver

    @abstractmethod
    def extract(self):
        pass

    def get_elements(self, selector):
        return utils.extract_list(
            self.driver.get_elements_or_none_by_selector(selector)
        )


class MessageExtractor(AbstractExtractor):
    """
    This class, `MessageExtractor`, is a subclass of `AbstractExtractor` and is
    responsible for extracting messages from a source.
    """
    pattern = r"[.!?;-]"

    def extract(self):
        raw_messages = self.get_elements(const.SELECTORS["message"])
        new_messages = []
        for message in raw_messages:
            message = re.sub(r"https?://.*", "", message)
            parts = re.split(self.pattern, message)
            new_message = parts[0] + parts[1] if len(
                parts[0]) < const.MINIMUM_MESSAGE_SIZE and len(parts) > 1 else parts[0]
            new_messages.append(new_message.strip())
        return new_messages


class HourExtractor(AbstractExtractor):
    """A class that extracts hours from a given input string."""
    pattern = re.compile(r"\d{2}:\d{2}")

    def extract(self):
        raw_hours = self.get_elements(const.SELECTORS["hour"])
        hours = self.pattern.findall(" ".join(raw_hours))
        filtered_hours = []
        i = 0
        while i < len(hours):
            if i < len(hours) - 1 and hours[i] == hours[i + 1]:
                i += 2
            else:
                filtered_hours.append(hours[i])
                i += 1
        return filtered_hours


class ReactionExtractor(AbstractExtractor):
    """
    The ReactionExtractor class is a subclass of the AbstractExtractor class.
    It provides methods to extract reactions from a web page.
    """
    pattern = re.compile(r"[\d.,]+")

    def extract(self):
        raw_reactions = self.driver.get_elements_or_none_by_selector(
            const.SELECTORS["reactions"]
        )
        raw_reactions_texts = [element.get_attribute("aria-label") for element in
                               raw_reactions]
        emojis = [[emoji.get_attribute("alt") for emoji in
                   element.find_elements(by="tag name", value="img")] for element in
                  raw_reactions]
        results = []
        for i, text in enumerate(raw_reactions_texts):
            numbers = self.pattern.findall(text)
            numbers = [number.replace(".", "") for number in numbers]
            total = int(numbers[-1]) if numbers else 0
            results.append((emojis[i], total))
        return results


class ChannelExtractor(AbstractExtractor):
    """This class is used to extract channels from a channel list."""
    def extract(self):
        channel_list = self.driver.get_element_or_none_by_selector(
            const.SELECTORS["channel_list"], wait=const.LONG_TIME)
        channels = channel_list.find_elements("css selector",
                                              const.SELECTORS["channel"])
        return {utils.simplify_channel_name(
            channel.get_attribute("title")): const.CHANNEL_TEMPLATE.substitute(
            channel=channel.get_attribute("title")) for channel in channels}
