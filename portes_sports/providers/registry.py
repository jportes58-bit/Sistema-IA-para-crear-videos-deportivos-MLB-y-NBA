from __future__ import annotations
from . import mlb, nba, manual

PROVIDERS = {
    "mlb_public": mlb.fetch,
    "nba_public": nba.fetch,
    "manual": manual.fetch,
}

def fetch_sport(provider_name: str, day: str | None = None) -> list[dict]:
    provider = PROVIDERS.get(provider_name, manual.fetch)
    return provider(day)
