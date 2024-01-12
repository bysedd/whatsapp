import re

from botasaurus import AntiDetectDriver

import src.constants as const
import src.utils as utils


def get_messages(driver: AntiDetectDriver) -> list[str]:
    """
    Get the content of the messages in the Whatsapp Channel.

    :param driver: The AntiDetectDriver object representing the web driver.
    :return: A list of the messages in the driver.
    """
    raw_messages = utils.extract_list(
        driver.get_elements_or_none_by_selector(const.SELECTORS["message"])
    )
    pattern = r"[.!?;-]"
    new_messages = []
    for message in raw_messages:
        # Remove any URLs from the message
        message = re.sub(r"https?://.*", "", message)

        # Split the message into parts
        parts = re.split(pattern, message)

        # If the first part is shorter than 20 characters, join the first two parts
        # together
        if len(parts[0]) < const.MINIMUM_MESSAGE_SIZE and len(parts) > 1:
            new_message = parts[0] + parts[1]
        else:
            new_message = parts[0]

        new_messages.append(new_message.strip())

    return new_messages


def get_hour(driver: AntiDetectDriver) -> list[str]:
    """
    Get the hours from the web page using a given driver.

    :param driver: The driver used to interact with the web page.
    :return: A list of filtered hours in HH:MM format.
    """
    raw_hours = utils.extract_list(
        driver.get_elements_or_none_by_selector(const.SELECTORS["hour"])
    )

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
    raw_elements = driver.get_elements_or_none_by_selector(const.SELECTORS["reactions"])
    raw_reactions = [element.get_attribute("aria-label") for element in raw_elements]

    emojis = [
        [
            emoji.get_attribute("alt")
            for emoji in element.find_elements(by="tag name", value="img")
        ]
        for element in raw_elements
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
        const.SELECTORS["channel_list"], wait=const.LONG_TIME
    )
    channels = channel_list.find_elements("css selector", const.SELECTORS["channel"])
    return {
        utils.simplify_channel_name(
            channel.get_attribute("title")
        ): const.CHANNEL_TEMPLATE.substitute(channel=channel.get_attribute("title"))
        for channel in channels
    }
