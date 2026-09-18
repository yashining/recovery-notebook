import unittest

from oura_chat.analysis import normalize_oura_data


class NormalizeOuraDataTests(unittest.TestCase):
    def test_keeps_analysis_fields_and_discards_identifiers(self) -> None:
        raw = {
            "daily_sleep": [
                {"id": "secret-id", "day": "2026-09-17", "score": 82, "contributors": {}}
            ],
            "daily_readiness": [{"day": "2026-09-17", "score": 77}],
            "daily_activity": [{"day": "2026-09-17", "steps": 9000}],
            "sleep": [
                {
                    "id": "another-secret-id",
                    "day": "2026-09-17",
                    "average_hrv": 41,
                    "heart_rate": {"interval": 300, "items": [55, 54]},
                }
            ],
        }

        normalized = normalize_oura_data(raw)

        self.assertEqual(normalized["daily_sleep"][0]["score"], 82)
        self.assertEqual(normalized["sleep_periods"][0]["average_hrv"], 41)
        self.assertNotIn("id", normalized["daily_sleep"][0])
        self.assertNotIn("heart_rate", normalized["sleep_periods"][0])

    def test_missing_collections_become_empty_lists(self) -> None:
        self.assertEqual(
            normalize_oura_data({}),
            {
                "daily_sleep": [],
                "daily_readiness": [],
                "daily_activity": [],
                "sleep_periods": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
