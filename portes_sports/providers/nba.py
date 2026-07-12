from __future__ import annotations
import requests

URL = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

def fetch(day: str | None = None) -> list[dict]:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nba.com/",
    }
    response = requests.get(URL, headers=headers, timeout=20)
    response.raise_for_status()

    stories: list[dict] = []
    for game in response.json().get("scoreboard", {}).get("games", []):
        away = game.get("awayTeam", {})
        home = game.get("homeTeam", {})
        stories.append({
            "sport": "NBA",
            "headline": f'{away.get("teamName", "Visitante")} vs {home.get("teamName", "Local")}',
            "summary": (
                f'Estado: {game.get("gameStatusText", "Sin información")}. '
                f'Marcador: {away.get("score", "-")} - {home.get("score", "-")}.'
            ),
            "source": "NBA Public Scoreboard",
        })
    return stories
