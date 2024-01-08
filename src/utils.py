import re

from src.constants import selectors, PATH
from botasaurus import AntiDetectDriver


# region Auxiliary functions
def extract_list(list_elements: list) -> list[str]:
    """
    Extracts a list of strings from a given list of elements.

    :param list_elements: A list of elements from which to extract strings.
    :return: A list of strings extracted from the given list of elements.
    """
    # Regex pattern to find consecutive whitespace
    pattern = re.compile(r"\s+")
    return [pattern.sub(" ", element.text.strip()) for element in list_elements]


def valid_channel(channel: str) -> bool:
    """
    Check if the specified channel is valid.

    :param channel: The channel to be checked.
    :return: True if the channel is valid, False otherwise.
    """
    try:
        return bool(selectors["channels"][channel])
    except KeyError:
        print(f"Invalid channel: '{channel}'")
        return False


def secure_open_write(*, file_name: str):
    """
    Open a file for secure writing.

    :param file_name: The name of the file to be created.
    :return: A file object opened in "write" mode.
    :raises ValueError: If disallowed, characters are detected in the file name.
    """
    disallowed_chars = ['..', '/', '\\']
    if any(char in file_name for char in disallowed_chars):
        raise ValueError(f"Disallowed characters detected in file name: {file_name}")

    full_path = PATH / "output" / f"data_{file_name}.csv"
    return open(full_path, "w")


# endregion

# region Functions that help the bot

def get_messages(driver: AntiDetectDriver) -> list[str]:
    """
    Get the content of the messages in the Whatsapp Channel.

    :param driver: The AntiDetectDriver object representing the web driver.
    :return: A list of the messages in the driver.
    """
    raw_messages = extract_list(
        driver.get_elements_or_none_by_selector(selectors["message"])
    )
    refined_messages = [re.split(r"[.!?;]", message)[0]
                        for message in raw_messages]
    return [re.sub(r"http://.*", "", message).strip()
            for message in refined_messages]


def get_hour(driver: AntiDetectDriver) -> list[str]:
    """
    Get the hours from the web page using a given driver.

    :param driver: The driver used to interact with the web page.
    :return: A list of filtered hours in HH:MM format.
    """
    raw_hours = extract_list(driver.get_elements_or_none_by_selector(selectors["hour"]))

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
    raw_elements = driver.get_elements_or_none_by_selector(selectors["reactions"])
    raw_reactions = [element.get_attribute("aria-label") for element in raw_elements]

    # region Extract emoji and total reactions
    # Pattern for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U0001F1F2"
        "\U0001F1F4"
        "\U0001F620"
        "\U0001F916"
        "]+",
        flags=re.UNICODE,
    )

    # Pattern for numbers, including possible dot or comma
    number_pattern = re.compile(r"[\d.,]+")

    result = []
    for text in raw_reactions:
        # Find all emojis in the string
        emojis = emoji_pattern.findall(text)

        # Find all numbers in the string
        numbers = number_pattern.findall(text)

        # Remove dots and commas in each number
        numbers = [number.replace(".", "").replace(",", "") for number in numbers]

        # Append a tuple of emojis and number to the result list
        result.append((emojis, int(numbers[-1])))

    # endregion

    return result

# endregion
