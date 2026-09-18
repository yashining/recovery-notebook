from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigurationError(ValueError):
    """Raised when required runtime configuration is absent."""


@dataclass(frozen=True)
class Settings:
    oura_access_token: str
    openai_api_key: str
    openai_model: str

    @classmethod
    def from_environment(cls) -> "Settings":
        missing = [
            name
            for name in ("OURA_ACCESS_TOKEN", "OPENAI_API_KEY")
            if not os.environ.get(name)
        ]
        if missing:
            joined = ", ".join(missing)
            raise ConfigurationError(f"Missing required environment variables: {joined}")

        return cls(
            oura_access_token=os.environ["OURA_ACCESS_TOKEN"],
            openai_api_key=os.environ["OPENAI_API_KEY"],
            openai_model=os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
        )
