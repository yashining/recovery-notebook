from __future__ import annotations

import json
from datetime import date
from typing import Any


INSTRUCTIONS = """You are a careful personal wellness data analyst.
Answer only from the supplied Oura records. State when records are missing or do not
support a conclusion. Use dates and concrete values as evidence. Distinguish observed
association from causation. Durations in Oura data are seconds unless the field says
otherwise; translate them into readable hours or minutes when useful. The final day
may be partial, especially for activity. Do not diagnose disease, prescribe treatment,
or overstate consumer wearable measurements. If the user raises symptoms or asks for
medical decisions, recommend an appropriate licensed clinician. Keep the answer
concise and directly answer the question."""


def answer_question(
    *,
    question: str,
    data: dict[str, Any],
    start_date: date,
    end_date: date,
    api_key: str,
    model: str,
) -> str:
    # Keep the optional third-party import at the API boundary so local unit tests can
    # exercise the rest of the project before dependencies or credentials are present.
    from openai import OpenAI

    payload = json.dumps(data, separators=(",", ":"), sort_keys=True)
    prompt = (
        f"Question: {question}\n"
        f"Inclusive data window: {start_date.isoformat()} through {end_date.isoformat()}\n"
        f"Oura records: {payload}"
    )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        input=prompt,
        store=False,
    )
    return response.output_text
