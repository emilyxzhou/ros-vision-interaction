#!/usr/bin/env python
import logging
import random
from interaction_engine.utils import make_sure_is_list

logging.basicConfig(level=logging.INFO)


class Message(object):
    class Type:
        MULTIPLE_CHOICE = "multiple choice"
        MULTIPLE_CHOICE_ONE_COLUMN = "multiple choice one column"
        TEXT_ENTRY = "text entry"
        NO_INPUT = "no input"

    def __init__(
            self,
            content
,
            message_type,
            keys_to_read=[],
            options=[],
            default_input=None,
    ):

        self._content = make_sure_is_list(content
                    )

        self._message_type = self._check_type(message_type)
        self._keys_to_read = self._check_keys_to_read(keys_to_read)
        self._options = self._check_options_correspond_to_type(self._message_type, options)
        self._check_database_keys_match_content()

        self._args = []

        self._default_input = self._check_default_input_is_valid(default_input)

    def _check_type(self, message_type):
        valid_types = [
            self.Type.MULTIPLE_CHOICE,
            self.Type.MULTIPLE_CHOICE_ONE_COLUMN,
            self.Type.TEXT_ENTRY,
            self.Type.NO_INPUT,
        ]
        if message_type not in valid_types:
            raise TypeError("Message type must be one of the following: {}".format(valid_types))
        return message_type

    def _check_keys_to_read(self, keys_to_read):
        keys_to_read = make_sure_is_list(keys_to_read)
        return keys_to_read

    def _check_options_correspond_to_type(self, message_type, options):
        if message_type in [self.Type.MULTIPLE_CHOICE, self.Type.MULTIPLE_CHOICE_ONE_COLUMN]:
            if len(options) == 0:
                raise IOError("Must have options for 'multiple choice' message.")
        elif message_type in [self.Type.TEXT_ENTRY, self.Type.NO_INPUT]:
            if len(options) > 1:
                raise IOError("Must have at most one option for text entry message.")
            options = ["Next"]
        return make_sure_is_list(options)

    def _check_database_keys_match_content(self):
        if self._keys_to_read is not None:
            data = {key: "" for key in self._keys_to_read}
            for content in self._content:
                try:
                    message = content.format(**data)
                except KeyError:
                    raise KeyError("Database keys \"{}\" do not match content keywords.".format(self._keys_to_read))

    def _check_default_input_is_valid(self, default_input):
        if self._message_type in [self.Type.MULTIPLE_CHOICE, self.Type.MULTIPLE_CHOICE_ONE_COLUMN]:
            if default_input is None:
                return self._options[0]
            else:
                if default_input not in self._options:
                    raise ValueError("Default input must be a valid option.")
        else:
            return ""

    def __repr__(self):
        return "Message: {}, Type: {}, Options: {}".format(
            self._content,
            self._message_type,
            self._options,
        )

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = make_sure_is_list(content)

    @property
    def message_type(self):
        return self._message_type

    @property
    def keys_to_read(self):
        return self._keys_to_read

    @property
    def options(self):
        return self._options

    @property
    def args(self):
        return self._args

    @property
    def default_input(self):
        return self._default_input

    def get_random_content(self):
        return random.choice(self._content)


if __name__ == "__main__":
    multiple_choice_message = Message(
        content=[
            "Hello!",
            "Hi there!",
        ],
        message_type=Message.Type.MULTIPLE_CHOICE,
        options=[
            "Hello!",
            "Hey!",
        ],
    )
    text_entry_message = Message(
        content=["What's your name?"],
        message_type=Message.Type.TEXT_ENTRY,
    )
    no_input_message = Message(
        content="Have a good one!",
        message_type=Message.Type.NO_INPUT
    )
    print(multiple_choice_message)
    print(text_entry_message)
    print(no_input_message)
