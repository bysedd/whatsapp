import src.constants as const


def extract_list(list_elements: list) -> list[str]:
    """
    Extracts a list of strings from a given list of elements.
    """
    return [
        const.WHITESPACE_PATTERN.sub(" ", element.text.strip())
        for element in list_elements
    ]


def adjust_list_length(data_list: list, target_length: int) -> list:
    """
    Ensure the list matches the target length by removing or adding elements as
    necessary.
    """
    while len(data_list) > target_length:
        data_list.pop(0)
    return data_list


def align_message_data(
    messages: list[str], hours: list[str], reactions: list[tuple[list[str | None], int]]
):
    """
    Aligns the elements in the given lists.
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
    """
    name_without_spaces = const.SPACE_PATTERN.sub("_", channel_name)
    return const.SPLIT_PATTERN.split(name_without_spaces)[0]


def extract_data_to_dict(
    messages: list[str], hours: list[str], reactions: list[tuple[list[str | None], int]]
):
    """
    Extracts data from given parameters and returns a dictionary.

    :param messages: list of messages
    :param hours: list of hours
    :param reactions: list of reactions
    """
    emojis, total = reactions
    # Pad emojis with None if its length is less than 4
    emojis = (emojis + [None] * 4)[:4]
    return {
        "message": messages,
        "hour": hours,
        "emoji_1": emojis[0],
        "emoji_2": emojis[1],
        "emoji_3": emojis[2],
        "emoji_4": emojis[3],
        "total": total,
    }
