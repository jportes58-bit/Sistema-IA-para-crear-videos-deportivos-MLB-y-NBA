from __future__ import annotations
from datetime import date
import requests

# Scoreboard público utilizado por NBA.com. Puede cambiar; el panel permite entrada manual como respaldo.
BASE = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

def get_scoreboard(day: str | None = None) -> list[dict]:
    # El endpoint público principal sirve el scoreboard vigente. Para fechas históricas
    # se recomienda conectar SportsDataIO/Sportradar o ingresar la historia manualmente.
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.nba.com/"}
    r = requests.get(BASE, headers=headers, timeout=20)
    r.raise_for_status()
    games = []
    for g in r.json().get("scoreboard", {}).get("games", []):
        away, home = g["awayTeam"], g["homeTeam"]
        games.append({
            "league": "NBA",
            "game_id": g.get("gameId"),
            "date": g.get("gameTimeUTC"),
            "status": g.get("gameStatusText", ""),
            "away": away.get("teamName"),
            "home": home.get("teamName"),
            "away_score": away.get("score"),
            "home_score": home.get("score"),
            "headline": f'{away.get("teamName")} vs {home.get("teamName")}',
            "summary": f'Estado: {g.get("gameStatusText", "")}. '
                       f'Marcador: {away.get("score", "-")} - {home.get("score", "-")}.'
        })
    return games
