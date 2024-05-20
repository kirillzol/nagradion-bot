import requests
from src.date_handler import *
from src.Match import *

data_1 = {"tournaments[]": 35961}  # Высшая Лига

data_2 = {"tournaments[]": 35962}  # Первая Лига

data_3 = {"tournaments[]": 35963}  # Вторая Лига

Leagues = ["Высшая Лига", "Первая Лига", "Вторая Лига"]


class Handler:
    def __init__(self, data: dict) -> None:
        self.url1 = "https://mipt.nagradion.ru/_anon/match_feed/load_props"
        self.data = data

    def get_data(self) -> dict:
        res = requests.post(self.url1, data=self.data).json()
        return res

    def get_list_of_matches(self) -> dict:
        res = Handler.get_data(self)
        league = Leagues[(self.data["tournaments[]"] - 1) % 10]
        dict_of_matches = {idx: Match(league, val['home_team_name'], val['guest_team_name'], val["publicDate"]) for
                           idx, val in
                           enumerate(res["matches"])}
        return dict_of_matches

    def get_list_of_teams(self) -> list:
        l = []
        league = Leagues[(self.data["tournaments[]"] - 1) % 10]
        res = Handler.get_data(self)
        for val in res["matches"]:
            if val["home_team_name"] not in l:
                l.append(Team(val["home_team_name"], league))
            if val["home_team_name"] not in l:
                l.append(Team(val["guest_team_name"], league))
        return l


def get_nearest_match(team: str):
    list_of_matches = []
    for data in [data_1, data_2, data_3]:
        list_of_matches += Handler(data).get_list_of_matches().items()
    for i in range(len(list_of_matches)):
        if team in [list_of_matches[i][1].team1, list_of_matches[i][1].team2] and compare_dates(list_of_matches[i][1].date):
            return list_of_matches[i][1].date
    return "расписания еще нет"

