import requests
BASE="https://statsapi.mlb.com/api/v1"
def games(day):
    r=requests.get(f"{BASE}/schedule",params={"sportId":1,"date":day},timeout=20)
    r.raise_for_status()
    out=[]
    for d in r.json().get("dates",[]):
        for g in d.get("games",[]):
            a,h=g["teams"]["away"],g["teams"]["home"]
            out.append({"sport":"MLB","date":g.get("gameDate",day),"away":a["team"]["name"],"home":h["team"]["name"],"away_score":a.get("score"),"home_score":h.get("score"),"status":g.get("status",{}).get("detailedState",""),"source":"MLB Stats API"})
    return out
def teams():
    r=requests.get(f"{BASE}/teams",params={"sportId":1},timeout=20);r.raise_for_status()
    return [{"team":t.get("name",""),"recent_form":0.5,"attack_rating":50,"defense_rating":50,"availability":1.0,"elo":1500} for t in r.json().get("teams",[])]
