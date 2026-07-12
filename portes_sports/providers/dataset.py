from pathlib import Path
import pandas as pd
DATA=Path("data")
def read(name):
    p=DATA/name
    return [] if not p.exists() else pd.read_csv(p).fillna("").to_dict("records")
def games(sport,day):
    rows=[r for r in read("games.csv") if str(r.get("sport","")).upper()==sport.upper()]
    return [r for r in rows if str(r.get("date","")).startswith(day)] if day else rows
def teams(sport): return [r for r in read("teams.csv") if str(r.get("sport","")).upper()==sport.upper()]
def players(sport): return [r for r in read("players.csv") if str(r.get("sport","")).upper()==sport.upper()]
