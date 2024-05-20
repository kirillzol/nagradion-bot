from src.Team import *

class Match:
    def __init__(self, league: str, team1: Team, team2: Team, date: str):
        self.league = league
        self.team1 = team1
        self.team2 = team2
        self.date = date

    def __repr__(self):
        return (f"Match(league='{self.league}', "
                f"team1='{self.team1}', team2='{self.team2}', date='{self.date}')")

    def __eq__(self, other):
        return self.date == other