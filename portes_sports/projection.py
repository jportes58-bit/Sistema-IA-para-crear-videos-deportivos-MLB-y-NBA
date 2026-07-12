import math
def f(v,d=0.0):
    try:return float(v)
    except:return d
def project(home,away,sport):
    hi=.30*f(home.get("recent_form"),.5)+.20*f(home.get("attack_rating"),50)/100+.20*f(home.get("defense_rating"),50)/100+.15*f(home.get("availability"),1)+.15*f(home.get("elo"),1500)/2000+.05
    ai=.30*f(away.get("recent_form"),.5)+.20*f(away.get("attack_rating"),50)/100+.20*f(away.get("defense_rating"),50)/100+.15*f(away.get("availability"),1)+.15*f(away.get("elo"),1500)/2000
    hp=1/(1+math.exp(-max(-4,min(4,(hi-ai)*5))))
    base={"NBA":112,"MLB":4.5,"NFL":23,"FUTBOL":1.4,"LIDOM":4.2,"UFC":1,"TENIS":2}.get(sport,10)
    spread=abs(hp-(1-hp))
    return {"home_probability":round(hp*100,1),"away_probability":round((1-hp)*100,1),"home_score":round(base*(.8+hi*.45),1),"away_score":round(base*(.8+ai*.45),1),"confidence":"Alta" if spread>=.25 else "Media" if spread>=.12 else "Baja"}
