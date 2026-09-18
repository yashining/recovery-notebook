import os
import unittest
from unittest.mock import patch

from oura_chat.config import ConfigurationError, Settings


class SettingsTests(unittest.TestCase):
    def test_reports_all_missing_required_variables(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                ConfigurationError, "OURA_ACCESS_TOKEN, OPENAI_API_KEY"
            ):
                Settings.from_environment()

    def test_reads_environment_and_default_model(self) -> None:
        with patch.dict(
            os.environ,
            {"OURA_ACCESS_TOKEN": "oura", "OPENAI_API_KEY": "openai"},
            clear=True,
        ):
            settings = Settings.from_environment()

        self.assertEqual(settings.oura_access_token, "oura")
        self.assertEqual(settings.openai_api_key, "openai")
        self.assertEqual(settings.openai_model, "gpt-5.6-luna")


if __name__ == "__main__":
    unittest.main()
