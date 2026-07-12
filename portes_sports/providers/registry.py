from portes_sports.mlb import get_schedule
from portes_sports.nba import get_scoreboard

def fetch_sport(sport: str, day: str):
    if sport == "MLB":
        return get_schedule(day)
    if sport == "NBA":
        return get_scoreboard(day)
    return []
