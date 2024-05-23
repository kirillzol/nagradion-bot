class Team:
    def __init__(self, name: str, league: str):
        self.name = name
        self.league = league

    def __repr__(self):
        return f"Team(name='{self.name}', league='{self.league}')"

    def __eq__(self, other):
        return self.name == other