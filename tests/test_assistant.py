import sys
import types
import unittest
from datetime import date
from unittest.mock import patch

from oura_chat.assistant import answer_question


class FakeResponses:
    def __init__(self) -> None:
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        return types.SimpleNamespace(output_text="A concise answer")


class FakeOpenAI:
    last_instance = None

    def __init__(self, *, api_key):
        self.api_key = api_key
        self.responses = FakeResponses()
        FakeOpenAI.last_instance = self


class AnswerQuestionTests(unittest.TestCase):
    def test_sends_bounded_data_without_api_storage(self) -> None:
        fake_module = types.SimpleNamespace(OpenAI=FakeOpenAI)

        with patch.dict(sys.modules, {"openai": fake_module}):
            answer = answer_question(
                question="How was my sleep?",
                data={"daily_sleep": [{"day": "2026-09-17", "score": 82}]},
                start_date=date(2026, 9, 11),
                end_date=date(2026, 9, 17),
                api_key="test-key",
                model="test-model",
            )

        instance = FakeOpenAI.last_instance
        self.assertEqual(answer, "A concise answer")
        self.assertEqual(instance.api_key, "test-key")
        self.assertEqual(instance.responses.request["model"], "test-model")
        self.assertFalse(instance.responses.request["store"])
        self.assertIn("2026-09-11 through 2026-09-17", instance.responses.request["input"])
        self.assertIn("How was my sleep?", instance.responses.request["input"])


if __name__ == "__main__":
    unittest.main()
