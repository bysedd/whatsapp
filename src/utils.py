import re
from datetime import datetime

import src.constants as const


def extract_list(list_elements: list) -> list[str]:
    """
    Extracts the text content from a list of elements.

    :param list_elements: A list of elements from which text content will be extracted.
    :return: A list of strings containing the extracted text content.
    """
    return [
        const.WHITESPACE_PATTERN.sub(" ", element.text.strip())
        for element in list_elements
    ]


def adjust_list_length(data_list: list, target_length: int) -> list:
    """
    Adjusts the length of a given list to a specified target length.

    :param data_list: The list has to be adjusted.
    :param target_length: The desired length of the list.
    :return: The adjusted list.
    """
    while len(data_list) > target_length:
        data_list.pop(0)
    return data_list


def align_message_data(
    messages: list[str], hours: list[datetime], reactions: list[tuple[list[str], int]]
):
    """
    Aligns the message data to have the same length based on the shortest list among
    messages, hours, and reactions.

    :param messages: The list of messages.
    :param hours: The list of hours.
    :param reactions: The list of reactions.

    :return: A tuple containing the aligned lists of messages, hours, and reactions.
    """
    target_length = min(len(messages), len(hours), len(reactions))
    messages = adjust_list_length(messages, target_length)
    hours = adjust_list_length(hours, target_length)
    reactions = adjust_list_length(reactions, target_length)

    return messages, hours, reactions


def simplify_channel_name(channel_name: str) -> str:
    """
    Simplifies the channel name by replacing all spaces with underscores and
    splitting the name by period.

    :param channel_name: The channel name
    """
    name_without_extra_spaces = re.sub(" +", "_", channel_name)
    return const.SPLIT_PATTERN.split(name_without_extra_spaces)[0]


def extract_data_to_dict(
    message: str, hour: datetime, reactions: list[tuple[list[str], int]]
):
    """
    Extracts data from given parameters and returns a dictionary.

    :param message: Message content.
    :param hour: Hour of message.
    :param reactions: List of reactions
    """
    emojis, total = reactions
    # Pad emojis with None if its length is less than 4
    emojis = (emojis + [None] * 4)[:4]
    return {
        "message": message,
        "hour": hour.strftime("%H:%M"),
        "emoji_1": emojis[0],
        "emoji_2": emojis[1],
        "emoji_3": emojis[2],
        "emoji_4": emojis[3],
        "total": total,
    }
