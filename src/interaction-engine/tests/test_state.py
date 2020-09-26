import unittest

from interaction_engine.message import Message
from interaction_engine.state import State
from interaction_engine.utils import make_sure_is_list

valid_name = "test state"
valid_message_type = Message.Type.TEXT_ENTRY
valid_contents = ["Hello there!"]
valid_next_states = ["test state 2"]


class TestState(unittest.TestCase):
    def test_check_name(self):
        valid_names = [
            "state 1",
            "state 2",
            "state 3"
        ]
        for valid_name in valid_names:
            state = State(
                name=valid_name,
                message_type=valid_message_type,
                content=valid_contents,
                next_states=valid_next_states
            )
            self.assertEqual(valid_name, state.name)
        invalid_names = [
            1,
            [1, 2, 3],
            {1: "a", 2: "b"}
        ]
        for invalid_name in invalid_names:
            self.assertRaises(
                TypeError,
                State,
                name=invalid_name
            )

    def test_check_create_message(self):
        valid_message_types = [
            Message.Type.MULTIPLE_CHOICE,
            Message.Type.MULTIPLE_CHOICE_ONE_COLUMN,
            Message.Type.NO_INPUT,
            Message.Type.TEXT_ENTRY
        ]
        valid_contents = "Hello there!"
        valid_next_state = ["test state 2"]
        valid_transitions = [
            {"Hi!": "test state 2"},
            {"Hi!": "test state 2"},
            None,
            None
        ]
        expected_options = [
            ["Hi!"],
            ["Hi!"],
            ["Next"],
            ["Next"]
        ]
        for i in range(4):
            state = State(
                name=valid_name,
                message_type=valid_message_types[i],
                content=valid_contents,
                next_states=valid_next_state,
                transitions=valid_transitions[i]
            )
            self.assertEqual(make_sure_is_list(valid_contents), state.message.content)
            self.assertEqual(valid_message_types[i], state.message.message_type)
            self.assertEqual(expected_options[i], state.message.options)

    def test_check_default_input(self):
        valid_transitions = [
            {"Hello there!": "test state 2", "Hi!": "test state 2", "Hello!": "test state 2"},
            {"Good": "test state 2", "Bad": "test state 2", "Okay": "test state 2"}
        ]
        valid_options_list = [
            ["Hello there!", "Hi!", "Hello!"],
            ["Good", "Bad", "Okay"]
        ]
        for i in range(2):
            for j in range(len(valid_options_list[i])):
                state = State(
                    name=valid_name,
                    message_type=Message.Type.MULTIPLE_CHOICE,
                    content=valid_contents,
                    next_states=valid_next_states,
                    transitions=valid_transitions[i],
                    default_input=valid_options_list[i][j]
                )


if __name__ == '__main__':
    unittest.main()
