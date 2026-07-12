import requests
URL="https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
def games(day):
    r=requests.get(URL,headers={"User-Agent":"Mozilla/5.0","Referer":"https://www.nba.com/"},timeout=20);r.raise_for_status()
    out=[]
    for g in r.json().get("scoreboard",{}).get("games",[]):
        a,h=g.get("awayTeam",{}),g.get("homeTeam",{})
        out.append({"sport":"NBA","date":g.get("gameTimeUTC",day),"away":a.get("teamName","Visitante"),"home":h.get("teamName","Local"),"away_score":a.get("score"),"home_score":h.get("score"),"status":g.get("gameStatusText",""),"source":"NBA Public Scoreboard"})
    return out
def teams(): return []
