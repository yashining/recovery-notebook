import io
import json
import unittest
from datetime import date

from oura_chat.oura import ENDPOINTS, OuraClient


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class OuraClientTests(unittest.TestCase):
    def test_fetches_each_collection_with_dates_and_bearer_token(self) -> None:
        requests = []

        def opener(request, *, timeout):
            requests.append((request, timeout))
            return FakeResponse(json.dumps({"data": [{"day": "2026-09-17"}]}).encode())

        result = OuraClient("test-token", opener=opener).fetch_window(
            date(2026, 9, 11), date(2026, 9, 17)
        )

        self.assertEqual(set(result), set(ENDPOINTS))
        self.assertEqual(len(requests), 4)
        for request, timeout in requests:
            self.assertIn("start_date=2026-09-11", request.full_url)
            self.assertIn("end_date=2026-09-17", request.full_url)
            self.assertEqual(request.get_header("Authorization"), "Bearer test-token")
            self.assertEqual(timeout, 20)

    def test_rejects_reversed_date_window(self) -> None:
        client = OuraClient("test-token", opener=lambda *_args, **_kwargs: None)
        with self.assertRaisesRegex(ValueError, "start_date"):
            client.fetch_window(date(2026, 9, 18), date(2026, 9, 17))


if __name__ == "__main__":
    unittest.main()
