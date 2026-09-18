# Oura Chat

A deliberately small learning project: fetch a bounded window of your Oura data,
send only the useful fields to the OpenAI Responses API, and answer one question in
the terminal.

Here, “ChatGPT” means a ChatGPT-like question-and-answer experience built with the
OpenAI API. This version does not appear inside the chatgpt.com interface. If that
interface is the goal, a later increment can expose the same data functions through
a remote MCP server/connector hosted on the VM.

The current version is an MVP, not a medical product. It does not diagnose illness
or replace advice from a clinician.

## What the MVP does

```text
terminal question
      |
      v
Oura API (4 read-only requests)
      |
      v
small, normalized JSON window
      |
      v
OpenAI Responses API -> terminal answer
```

It intentionally has no database, browser UI, background job, model-controlled
tools, or production OAuth callback yet. The access token is supplied through the
environment. Oura has deprecated personal access tokens, so a new integration
should ultimately obtain this token through OAuth; that is the next milestone.

## Run it

Python 3.11 or newer is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

export OURA_ACCESS_TOKEN="..."
export OPENAI_API_KEY="..."

oura-chat --days 7 "How has my sleep and readiness changed this week?"
```

`--days` accepts 1 through 30 and defaults to 7. The window ends today in UTC;
today's activity may therefore be incomplete. To make a comparison reproducible,
set an explicit inclusive end date:

```bash
oura-chat --days 14 --end-date 2026-09-17 \
  "Compare the first and second weeks. Mention HRV and resting heart rate."
```

The default model is `gpt-5.6-luna`. Override it with `OPENAI_MODEL` without
changing code. API responses are requested with `store=False` because the payload
contains personal health data.

## Test it

The tests do not call Oura or OpenAI and do not need credentials:

```bash
python -m unittest discover -s tests -v
```

## Learning roadmap

Each increment should leave a working program and add one new idea.

1. **MVP: one bounded question.** Four Oura reads, normalization, one model call,
   one terminal answer. Acceptance: unit tests pass and a real seven-day question
   returns an evidence-based answer.
2. **OAuth bootstrap.** Add a local callback command, CSRF state validation, token
   exchange, refresh, and a root-readable token file. Acceptance: delete the token
   file, authorize once, then run the unchanged question command.
3. **Deterministic trends.** Compute averages, changes, and missing-data counts in
   Python before prompting. Acceptance: calculations have fixture-based tests and
   the model only explains numbers produced by code.
4. **Local history.** Sync Oura data into SQLite with idempotent upserts. Acceptance:
   repeat syncs create no duplicates and 90-day questions send aggregates rather
   than raw records.
5. **VM service.** Add a small authenticated HTTP interface and a systemd unit.
   Acceptance: it survives a reboot, binds only to the intended interface, and no
   secrets appear in source, logs, or process arguments.
6. **Conversation and richer tools.** Let the model request the precise date range
   and metrics it needs using function calling. Acceptance: tool arguments and
   outputs are logged without secrets and bounded by server-side limits.
7. **Optional ChatGPT connector.** Expose the bounded read functions through remote
   MCP if using the chatgpt.com interface is important. Acceptance: ChatGPT can call
   read-only tools through authenticated HTTPS without receiving Oura credentials.

This sequence keeps the data path visible. Frameworks, Docker, dashboards, vector
databases, and multi-user support can wait until a concrete need appears.

## Data and safety notes

- Treat Oura records and OAuth credentials as sensitive. Do not commit `.env` or
  token files.
- The application requests no email or profile data and sends only selected health
  fields for the chosen dates.
- Model output should be treated as a wellness-oriented interpretation, not a
  diagnosis. Concerning symptoms or sustained changes belong with a clinician.
- Review the current Oura API agreement and OpenAI data controls before exposing the
  project to other users.
