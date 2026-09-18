from __future__ import annotations

import json
from collections.abc import Callable
from datetime import date
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


OURA_API_BASE = "https://api.ouraring.com/v2/usercollection"
ENDPOINTS = ("daily_sleep", "daily_readiness", "daily_activity", "sleep")


class OuraAPIError(RuntimeError):
    """A safe, token-free description of an Oura API failure."""


class OuraClient:
    def __init__(
        self,
        access_token: str,
        *,
        opener: Callable[..., Any] = urlopen,
        timeout_seconds: float = 20,
    ) -> None:
        self._access_token = access_token
        self._opener = opener
        self._timeout_seconds = timeout_seconds

    def fetch_window(self, start_date: date, end_date: date) -> dict[str, list[dict[str, Any]]]:
        if start_date > end_date:
            raise ValueError("start_date must be on or before end_date")

        return {
            endpoint: self._fetch_collection(endpoint, start_date, end_date)
            for endpoint in ENDPOINTS
        }

    def _fetch_collection(
        self, endpoint: str, start_date: date, end_date: date
    ) -> list[dict[str, Any]]:
        query = urlencode(
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
        )
        request = Request(
            f"{OURA_API_BASE}/{endpoint}?{query}",
            headers={
                "Authorization": f"Bearer {self._access_token}",
                "Accept": "application/json",
                "User-Agent": "oura-chat/0.1",
            },
        )

        try:
            with self._opener(request, timeout=self._timeout_seconds) as response:
                payload = json.load(response)
        except HTTPError as error:
            raise OuraAPIError(f"Oura request to {endpoint} failed with HTTP {error.code}") from error
        except URLError as error:
            raise OuraAPIError(f"Could not reach Oura while requesting {endpoint}") from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise OuraAPIError(f"Oura returned invalid JSON for {endpoint}") from error

        data = payload.get("data")
        if not isinstance(data, list):
            raise OuraAPIError(f"Oura returned an unexpected payload for {endpoint}")
        return data
