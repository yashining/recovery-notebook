from __future__ import annotations

from typing import Any


DAILY_SLEEP_FIELDS = ("day", "score", "contributors", "timestamp")
READINESS_FIELDS = (
    "day",
    "score",
    "contributors",
    "temperature_deviation",
    "temperature_trend_deviation",
    "timestamp",
)
ACTIVITY_FIELDS = (
    "day",
    "score",
    "active_calories",
    "total_calories",
    "steps",
    "equivalent_walking_distance",
    "high_activity_time",
    "medium_activity_time",
    "low_activity_time",
    "sedentary_time",
    "resting_time",
    "non_wear_time",
    "target_calories",
    "target_meters",
    "contributors",
    "timestamp",
)
SLEEP_FIELDS = (
    "day",
    "type",
    "bedtime_start",
    "bedtime_end",
    "total_sleep_duration",
    "deep_sleep_duration",
    "rem_sleep_duration",
    "light_sleep_duration",
    "awake_time",
    "efficiency",
    "latency",
    "restless_periods",
    "average_breath",
    "average_heart_rate",
    "lowest_heart_rate",
    "average_hrv",
)


def _select(record: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: record[field] for field in fields if field in record}


def normalize_oura_data(raw: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Keep useful fields and discard identifiers and verbose time-series data."""
    return {
        "daily_sleep": [
            _select(record, DAILY_SLEEP_FIELDS) for record in raw.get("daily_sleep", [])
        ],
        "daily_readiness": [
            _select(record, READINESS_FIELDS)
            for record in raw.get("daily_readiness", [])
        ],
        "daily_activity": [
            _select(record, ACTIVITY_FIELDS) for record in raw.get("daily_activity", [])
        ],
        "sleep_periods": [
            _select(record, SLEEP_FIELDS) for record in raw.get("sleep", [])
        ],
    }
