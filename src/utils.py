import re

WHITESPACE_PATTERN = re.compile(r"\s+")
SPACE_PATTERN = re.compile(r"\s")
SPLIT_PATTERN = re.compile(r"[.!]")


def extract_list(list_elements: list) -> list[str]:
    """
    Extracts a list of strings from a given list of elements.
    """
    return [WHITESPACE_PATTERN.sub(" ", element.text.strip()) for element in
            list_elements]


def adjust_list_length(data_list: list, target_length: int):
    """
    Ensure the list matches the target length by removing or adding elements as necessary.
    """
    while len(data_list) < target_length:
        data_list.append(([], 0))
    while len(data_list) > target_length:
        data_list.pop(0)


def align_message_data(
        messages: list[str], hours: list[str],
        reactions: list[tuple[list[str | None], int]]
):
    """
    Aligns the elements in the given lists.
    """
    target_length = len(messages)
    adjust_list_length(reactions, target_length)
    adjust_list_length(hours, target_length)

    return messages, hours, reactions


def simplify_channel_name(channel_name: str) -> str:
    """
    Simplifies the channel name by replacing all spaces with underscores and
    splitting the name by period.
    """
    name_without_spaces = SPACE_PATTERN.sub("_", channel_name)
    return SPLIT_PATTERN.split(name_without_spaces)[0]