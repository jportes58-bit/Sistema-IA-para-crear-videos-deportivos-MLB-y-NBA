from __future__ import annotations
from datetime import date
import requests

BASE_URL = "https://statsapi.mlb.com/api/v1"

def fetch(day: str | None = None) -> list[dict]:
    chosen_day = day or date.today().isoformat()
    response = requests.get(
        f"{BASE_URL}/schedule",
        params={"sportId": 1, "date": chosen_day, "hydrate": "team,linescore"},
        timeout=20,
    )
    response.raise_for_status()

    stories: list[dict] = []
    for day_group in response.json().get("dates", []):
        for game in day_group.get("games", []):
            away = game["teams"]["away"]
            home = game["teams"]["home"]
            stories.append({
                "sport": "MLB",
                "headline": f'{away["team"]["name"]} vs {home["team"]["name"]}',
                "summary": (
                    f'Estado: {game.get("status", {}).get("detailedState", "Sin información")}. '
                    f'Marcador: {away.get("score", "-")} - {home.get("score", "-")}.'
                ),
                "source": "MLB Stats API",
            })
    return stories
