#!/usr/bin/env python
import logging
from interaction_engine.message import Message

logging.basicConfig(level=logging.INFO)


class State(object):

    def __init__(
            self,
            name,
            message_type,
            content,
            next_states,
            transitions=None,
            database_keys_to_read=[],
            default_input=None,
    ):

        if type(name) is not str:
            raise TypeError("Name must be a string.")
        self._name = name

        self._check_valid_inputs(database_keys_to_read, message_type)

        next_states = self._make_sure_next_states_match_type(message_type, next_states)
        self._next_states = []
        for next_state in next_states:
            self.add_next_state(next_state)

        self._transitions = self._make_sure_transitions_are_valid(message_type, transitions)

        self._database_key_to_write = self._name

        if default_input is not None:
            default_input = self._check_default_input(default_input, message_type, transitions)

        self._message = self._create_message(content, database_keys_to_read, message_type, transitions, default_input)

    def _check_valid_inputs(self, database_keys_to_read, message_type):
        valid_message_types = [
            Message.Type.MULTIPLE_CHOICE,
            Message.Type.MULTIPLE_CHOICE_ONE_COLUMN,
            Message.Type.TEXT_ENTRY,
            Message.Type.NO_INPUT,
        ]
        self._check_valid_message_type(message_type, valid_message_types)
        self._check_db_keys_are_valid(database_keys_to_read)

    def _check_valid_message_type(self, message_type, valid_message_types):
        if message_type not in valid_message_types:
            raise TypeError("Message type must be one of the following: {}".format(valid_message_types))

    def _check_db_keys_are_valid(self, database_keys_to_read):
        if database_keys_to_read is not None:
            if type(database_keys_to_read) is not list:
                raise TypeError("Database keys to read must be a list.")
            for key in database_keys_to_read:
                if type(key) is not str:
                    raise TypeError("Database keys must be strings.")

    def _make_sure_next_states_match_type(self, message_type, next_states):
        if type(next_states) is not list:
            raise TypeError("Next states must be a list.")
        else:
            if message_type not in [Message.Type.MULTIPLE_CHOICE, Message.Type.MULTIPLE_CHOICE_ONE_COLUMN]:
                if len(next_states) > 1:
                    raise IOError("Cannot have more than one next state for non-multiple-choice messages.")
        return next_states

    def add_next_state(self, next_state):
        if type(next_state) is not str:
            raise TypeError("Next state must be a string.")
        if next_state in self._next_states:
            raise ValueError("{} is already a next state.".format(next_state))
        self._next_states.append(next_state)

    def _make_sure_transitions_are_valid(self, message_type, transitions):
        if message_type in [Message.Type.MULTIPLE_CHOICE, Message.Type.MULTIPLE_CHOICE_ONE_COLUMN]:
            if len(transitions) == 0:
                raise ValueError("Multiple choice messages must have transitions.")
            if type(transitions) is not dict:
                raise TypeError("Transitions must be a dict for multiple choice messages.")
            else:
                for option in list(transitions.keys()):
                    if type(option) is not str:
                        raise TypeError("Transition keys must be strings.")
                for next_state in list(transitions.values()):
                    if next_state not in self._next_states:
                        raise ValueError("Transition values must be valid next states.")
        return self._make_transitions(message_type, transitions)

    def _make_transitions(self, message_type, transitions):
        if message_type in [Message.Type.MULTIPLE_CHOICE, Message.Type.MULTIPLE_CHOICE_ONE_COLUMN]:
            next_state_names = list(transitions.values())
            new_transitions = {i: next_state_names[i] for i in range(len(next_state_names))}
        else:
            if len(self._next_states) > 0:
                new_transitions = {0: self._next_states[0]}
            else:
                new_transitions = None
        return new_transitions

    def _create_message(self, content, database_keys_to_read, message_type, transitions, default_input):
        if message_type in [Message.Type.TEXT_ENTRY, Message.Type.NO_INPUT]:
            options = ["Next"]
        else:
            options = list(transitions.keys())

        return Message(
            content=content,
            message_type=message_type,
            keys_to_read=database_keys_to_read,
            options=options,
            default_input=default_input
        )

    def _check_default_input(self, default_input, message_type, transitions):
        if message_type == Message.Type.TEXT_ENTRY:
            if type(default_input) is not str:
                raise TypeError("Default input for text entry message must be a string")
        if message_type in [Message.Type.MULTIPLE_CHOICE, Message.Type.MULTIPLE_CHOICE_ONE_COLUMN]:
            if default_input not in transitions.keys():
                raise ValueError("Default input for multiple choice must be a valid option")

    def __repr__(self):
        return "State: {}, {}, Transitions: {}".format(self._name, self._message, self._transitions)

    @property
    def name(self):
        return self._name

    @property
    def next_states(self):
        return self._next_states

    @property
    def transitions(self):
        return self._transitions

    @property
    def message(self):
        return self._message

    @property
    def database_key_to_write(self):
        return self._database_key_to_write

    def get_next_state(self, user_input):
        if len(self._next_states) == 1:
            return self._next_states[0]
        else:
            return self._transitions[user_input]
