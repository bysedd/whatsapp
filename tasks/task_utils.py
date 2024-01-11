from botasaurus import AntiDetectDriver
from src.utils import extract_list, simplify_channel_name
from src.constants import SELECTORS, CHANNEL_TEMPLATE
import re


def get_messages(driver: AntiDetectDriver) -> list[str]:
    """
    Get the content of the messages in the Whatsapp Channel.

    :param driver: The AntiDetectDriver object representing the web driver.
    :return: A list of the messages in the driver.
    """
    raw_messages = extract_list(
        driver.get_elements_or_none_by_selector(SELECTORS["message"])
    )
    pattern = r"[.!?;-]"
    return [
        re.sub(
            r"https?://.*", "", (
                re.split(pattern, message)[0][:-1]
                if message.endswith(":")
                else re.split(pattern, message)[0])).strip()
        for message in raw_messages
    ]


def get_hour(driver: AntiDetectDriver) -> list[str]:
    """
    Get the hours from the web page using a given driver.

    :param driver: The driver used to interact with the web page.
    :return: A list of filtered hours in HH:MM format.
    """
    raw_hours = extract_list(driver.get_elements_or_none_by_selector(SELECTORS["hour"]))

    # Regex to find times in HH:MM format
    time_pattern = re.compile(r"\d{2}:\d{2}")
    # Extract the schedules and form a list
    hours = time_pattern.findall(" ".join(raw_hours))

    # Create a new list to keep filtered hours
    filtered_hours = []
    i = 0
    while i < len(hours):
        # If the current hour is the same as the next hour, skip both
        if i < len(hours) - 1 and hours[i] == hours[i + 1]:
            i += 2
        else:
            filtered_hours.append(hours[i])
            i += 1

    return filtered_hours


def get_reactions(driver: AntiDetectDriver) -> list[tuple[list[str], int]]:
    """
    :param driver: An instance of AntiDetectDriver used to interact with the web page.
    :return: A list of tuples, where each tuple contains two elements:
             - A list of emojis found in the reaction string.
             - The total number of reactions.
    """
    raw_elements = driver.get_elements_or_none_by_selector(SELECTORS["reactions"])
    raw_reactions = [element.get_attribute("aria-label") for element in raw_elements]

    emojis = [
        [
            emoji.get_attribute("alt")
            for emoji in element.find_elements(by='tag name', value='img')
        ] for element in raw_elements
    ]

    # Pattern for numbers, including possible dot or comma
    number_pattern = re.compile(r"[\d.,]+")

    result = []
    for i, text in enumerate(raw_reactions):
        # Find all numbers in the string
        numbers = number_pattern.findall(text)
        # Remove dots in each number
        numbers = [number.replace(".", "") for number in numbers]
        # Check if a number list is not empty, else assign 0 as the default total
        total = int(numbers[-1]) if numbers else 0
        # Append a tuple of emojis and number to the result list
        result.append((emojis[i], total))

    return result


def get_channels(driver: AntiDetectDriver) -> dict[str, str]:
    """
    Get the available channels from the web page using a given driver.

    :param driver: The driver used to interact with the web page.
    :return: A list of available channels.
    """
    channel_list = driver.get_element_or_none_by_selector(
        SELECTORS['channel_list']
    )
    channels = channel_list.find_elements('css selector', SELECTORS['channel'])
    return {
        simplify_channel_name(channel.get_attribute("title")):
            CHANNEL_TEMPLATE.substitute(
                channel=channel.get_attribute("title")
            )
        for channel in channels
    }
