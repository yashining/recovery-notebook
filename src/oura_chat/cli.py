from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta, timezone

from .analysis import normalize_oura_data
from .assistant import answer_question
from .config import ConfigurationError, Settings
from .oura import OuraAPIError, OuraClient


def _iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected YYYY-MM-DD") from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oura-chat",
        description="Ask one question about a bounded window of your Oura data.",
    )
    parser.add_argument("question", help="question to answer from the selected data")
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        choices=range(1, 31),
        metavar="1-30",
        help="number of days to fetch (default: 7)",
    )
    parser.add_argument(
        "--end-date",
        type=_iso_date,
        default=None,
        help="inclusive end date as YYYY-MM-DD (default: today in UTC)",
    )
    return parser


def run(args: argparse.Namespace) -> str:
    settings = Settings.from_environment()
    end_date = args.end_date or datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=args.days - 1)

    raw_data = OuraClient(settings.oura_access_token).fetch_window(start_date, end_date)
    data = normalize_oura_data(raw_data)
    return answer_question(
        question=args.question,
        data=data,
        start_date=start_date,
        end_date=end_date,
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        print(run(args))
    except (ConfigurationError, OuraAPIError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
