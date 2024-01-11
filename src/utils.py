import re


def extract_list(list_elements: list) -> list[str]:
    """
    Extracts a list of strings from a given list of elements.

    :param list_elements: A list of elements from which to extract strings.
    :return: A list of strings extracted from the given list of elements.
    """
    # Regex pattern to find consecutive whitespace
    pattern = re.compile(r"\s+")
    return [pattern.sub(" ", element.text.strip()) for element in list_elements]


def align_elements(
        messages: list[str], hours: list[str],
        reactions: list[tuple[list[str | None], int]]
):
    """
    Aligns the elements in the given lists.

    :param messages: A list of strings representing messages.
    :param hours: A list of strings representing hours.
    :param reactions: A list of tuple consisting of a list of strings and an integer.
    :return: A tuple of the aligned lists: messages, hours, and reactions.
    """
    if len(reactions) > len(messages):
        reactions.pop(0)
    if len(reactions) < len(messages):
        reactions.append(([], 0))
    if len(hours) > len(messages):
        hours.pop(0)

    new_reactions = []
    previous_emojis = None
    for reaction in reactions:
        emojis = reaction[0]
        if emojis != previous_emojis:
            new_reactions.append(reaction)
            previous_emojis = emojis
    reactions = new_reactions

    return messages, hours, reactions


def simplify_channel_name(channel_name: str) -> str:
    """
    Simplifies the channel name by replacing all spaces with underscores and
    splitting the name by period.

    :param channel_name: The original channel name.
    :return: The simplified channel name.
    """
    name_without_spaces = re.sub(r"\s", "_", channel_name)
    return re.split(r'[.]', name_without_spaces)[0]
