from . import mlb,nba,dataset
def get_games(sport,provider,day):
    if provider=="mlb_public": return mlb.games(day)
    if provider=="nba_public": return nba.games(day)
    return dataset.games(sport,day)
def get_teams(sport,provider):
    if provider=="mlb_public": return mlb.teams()
    if provider=="nba_public": return nba.teams()
    return dataset.teams(sport)
def get_players(sport,provider): return dataset.players(sport)
