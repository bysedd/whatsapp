from botasaurus import *
from src.utils import *
from time import sleep


@browser(profile="whatsapp", headless=False, block_images=True)
def main_task(driver: AntiDetectDriver, data):
    driver.maximize_window()

    driver.organic_get("https://web.whatsapp.com/")
    driver.click(selectors["channels_button"], wait=99)
    driver.click(selectors["channels"]["tv_globo"])
    sleep(10)

    message_content = extract_list(get_content(driver))
    hour_message = extract_list(get_hour(driver))

    print(message_content[-1])
    print(hour_message[-1])

    sleep(5)


def get_content(driver: AntiDetectDriver):
    """
    :param driver: The AntiDetectDriver instance used to interact with the web page.
    :return: The elements, if any, found by the given selector for the message content.

    """
    return driver.get_elements_or_none_by_selector(selectors['message_content'])


def get_hour(driver: AntiDetectDriver):
    """
    :param driver: An instance of the AntiDetectDriver class that is used to interact with the browser.
    :return: A list of elements that match the selector for the hour message.
    """
    return driver.get_elements_or_none_by_selector(selectors['hour_message'])


