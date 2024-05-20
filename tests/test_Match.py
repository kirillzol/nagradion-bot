from src.Match import Match
from src.Team import Team
import pytest


def test_match_init():
    league = "Высшая Лига"
    team1 = Team(name="Профессура", league=league)
    team2 = Team(name="Машина", league=league)
    date = "Пт 03.05 20:00"

    match = Match(league=league, team1=team1, team2=team2, date=date)

    assert match.league == league
    assert match.team1 == team1
    assert match.team2 == team2
    assert match.date == date


def test_match_repr():
    league = "Высшая Лига"
    team1 = Team(name="Машина", league=league)
    team2 = Team(name="Профессура", league=league)
    date = "Пт 03.05 20:00"

    match = Match(league=league, team1=team1, team2=team2, date=date)

    expected_repr = ("Match(league='Высшая Лига', "
                     "team1='Team(name='Машина', league='Высшая Лига')', "
                     "team2='Team(name='Профессура', league='Высшая Лига')', "
                     "date='Пт 03.05 20:00')")
    assert repr(match) == expected_repr


def test_match_eq():
    league = "Высшая Лига"
    team1 = Team(name="Профессура", league=league)
    team2 = Team(name="Машина", league=league)
    date1 = "Пт 03.05 20:00"
    date2 = "Сб 04.05 18:00"

    match1 = Match(league=league, team1=team1, team2=team2, date=date1)
    match2 = Match(league=league, team1=team1, team2=team2, date=date1)
    match3 = Match(league=league, team1=team1, team2=team2, date=date2)

    assert match1 == match2
    assert match1 != match3
