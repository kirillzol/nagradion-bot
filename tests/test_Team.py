import pytest
from src.Team import Team


def test_team_initialization():
    team = Team(name="Машина", league="Певая Лига")
    assert team.name == "Машина"
    assert team.league == "Певая Лига"


def test_team_repr():
    team = Team(name="Машина", league="Певая Лига")
    assert repr(team) == "Team(name='Машина', league='Певая Лига')"


def test_team_equality():
    team = Team(name="Машина", league="Певая Лига")
    assert team == "Машина"
    assert not (team == "ФФФ")
