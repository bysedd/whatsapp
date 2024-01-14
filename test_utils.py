import unittest
from unittest.mock import MagicMock
import src.utils as utils


class TestUtils(unittest.TestCase):

    def test_extract_list(self):
        elements = [MagicMock(text='  extraneous   whitespace  '),
                    MagicMock(text='  more   spaces  ')]
        extracted = utils.extract_list(elements)
        expected = ['extraneous whitespace', 'more spaces']
        self.assertListEqual(extracted, expected)

    def test_adjust_list_length(self):
        data_list = [1, 2, 3, 4, 5]
        adjusted = utils.adjust_list_length(data_list, 3)
        expected_list = [3, 4, 5]
        self.assertListEqual(adjusted, expected_list)

    def test_adjust_list_length_no_adjustment_needed(self):
        data_list = ['a', 'b']
        adjusted = utils.adjust_list_length(data_list, 2)
        expected_list = ['a', 'b']
        self.assertListEqual(adjusted, expected_list)

    def test_align_message_data(self):
        messages = ['message1', 'message2', 'message3']
        hours = ['hour1', 'hour2']
        reactions = [(['reaction1', 'reaction2', None, None], 12)]
        aligned_messages, aligned_hours, aligned_reactions = utils.align_message_data(
            messages, hours, reactions)
        self.assertListEqual(aligned_messages, [messages[-1]])
        self.assertListEqual(aligned_hours, [hours[-1]])
        self.assertListEqual(aligned_reactions, [reactions[-1]])

    def test_simplify_channel_name(self):
        simple_name = utils.simplify_channel_name('channel   name.ignored')
        self.assertEqual(simple_name, 'channel_name')

    def test_extract_data_to_dict(self):
        messages = ['message']
        hours = ['hour']
        reactions = [['😂', '😍'], 2]
        data_dict = utils.extract_data_to_dict(messages, hours, reactions)
        expected_dict = {
            "message": messages,
            "hour": hours,
            "emoji_1": '😂',
            "emoji_2": '😍',
            "emoji_3": None,
            "emoji_4": None,
            "total": 2,
        }
        self.assertDictEqual(data_dict, expected_dict)


if __name__ == "__main__":
    unittest.main()
