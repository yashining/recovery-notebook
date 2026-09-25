# Privacy Policy

Effective date: September 25, 2026

## Scope and operator

Recovery Notebook is a personal, single-user, self-hosted learning project
operated by the owner of the
[yashining/recovery-notebook](https://github.com/yashining/recovery-notebook)
repository. This policy describes how the current application handles data.

## Data processed

Recovery Notebook processes:

- an access token used to authenticate requests to the Oura API;
- the sleep, readiness, activity, heart-rate, and HRV-related records authorized
  by the user;
- questions the user asks about those records; and
- answers generated for those questions.

The current application does not request Oura email or profile data.

## How data is used

The data is used only to retrieve the user's authorized records, reduce them to
fields relevant to the question, and generate personal wellness summaries and
trend explanations. Recovery Notebook does not sell data, use it for advertising,
or use it to train or fine-tune an AI model.

The application's output is informational and is not a medical diagnosis or a
substitute for advice from a qualified healthcare professional.

## Data disclosure

Recovery Notebook retrieves authorized records from the Oura API. It sends the
user's question and selected Oura fields to the OpenAI API to generate an answer.
It does not send the Oura access token to OpenAI.

The OpenAI API is called with response storage disabled (`store=false`). OpenAI
states that API data is not used to train its models unless the customer explicitly
opts in. OpenAI may nevertheless retain prompts and responses in abuse-monitoring
logs for up to 30 days under its standard data controls. See
[OpenAI's API data controls](https://developers.openai.com/api/docs/guides/your-data)
for current details.

No other disclosure is intended unless required by law.

## Storage and retention

The current application has no database and does not intentionally retain Oura
records, questions, or generated answers after a command finishes. Data is held in
memory while processing a request.

The Oura access token remains in the operator-controlled runtime environment until
it is removed, replaced, expired, or revoked. Data handled by Oura and OpenAI is
subject to those providers' respective retention practices.

If a future version stores health records or conversation history, this policy will
be updated before that feature is enabled.

## User choices and deletion

The user controls which Oura scopes are authorized and may revoke the application's
access through Oura. Removing the local access token prevents further API access.

To request access to or deletion of any operator-controlled data, open an issue in
the [repository issue tracker](https://github.com/yashining/recovery-notebook/issues).
Do not include health data, credentials, or other sensitive information in a public
issue. Operator-controlled user data will be deleted within 72 hours of a verified
request. Recovery Notebook cannot directly delete records retained by Oura or
OpenAI under their own policies.

## Security

Credentials are supplied outside the source repository, API requests use HTTPS,
and the application sends only selected fields needed for its purpose. No method of
storage or transmission is completely secure.

## Changes

Material changes will be published in this repository with an updated effective
date.

## Contact

Privacy questions may be submitted through the
[repository issue tracker](https://github.com/yashining/recovery-notebook/issues)
without including private health or credential information.
