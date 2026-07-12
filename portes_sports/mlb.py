from __future__ import annotations
from datetime import date
import requests

BASE = "https://statsapi.mlb.com/api/v1"

def get_schedule(day: str | None = None) -> list[dict]:
    day = day or date.today().isoformat()
    params = {
        "sportId": 1,
        "date": day,
        "hydrate": "team,linescore,decisions"
    }
    r = requests.get(f"{BASE}/schedule", params=params, timeout=20)
    r.raise_for_status()
    payload = r.json()
    games = []
    for d in payload.get("dates", []):
        for g in d.get("games", []):
            away = g["teams"]["away"]
            home = g["teams"]["home"]
            games.append({
                "league": "MLB",
                "game_id": g.get("gamePk"),
                "date": g.get("gameDate"),
                "status": g.get("status", {}).get("detailedState", ""),
                "away": away["team"]["name"],
                "home": home["team"]["name"],
                "away_score": away.get("score"),
                "home_score": home.get("score"),
                "headline": f'{away["team"]["name"]} vs {home["team"]["name"]}',
                "summary": f'Estado: {g.get("status", {}).get("detailedState", "")}. '
                           f'Marcador: {away.get("score", "-")} - {home.get("score", "-")}.'
            })
    return games
