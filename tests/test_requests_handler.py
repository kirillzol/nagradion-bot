import pytest
from unittest.mock import patch
from src.requests_handler import Handler, get_nearest_match, data_1, data_2, data_3
from src.Match import Match
from src.Team import Team

mocked_response = {
    "matches": [
        {"home_team_name": "Машина", "guest_team_name": "Landragons", "publicDate": "Пт 03.05 20:00"},
        {"home_team_name": "Аль-МФТИляль", "guest_team_name": "ИНБИКСТ", "publicDate": "Сб 04.05 18:00"}
    ]
}


@patch('src.requests_handler.requests.post')
def test_get_data(mock_post):
    mock_post.return_value.json.return_value = mocked_response
    handler = Handler(data_1)
    data = handler.get_data()
    assert data == mocked_response


@patch('src.requests_handler.requests.post')
def test_get_list_of_matches(mock_post):
    mock_post.return_value.json.return_value = mocked_response
    handler = Handler(data_1)
    matches = handler.get_list_of_matches()
    m1 = Match("Первая Лига", Team("Машина", "Первая Лига"), Team("Landragons", "Первая Лига"), "Пт 03.05 20:00"),
    m2 = Match("Первая Лига", Team("Аль-МФТИляль", "Первая Лига"), Team("ИНБИКСТ", "Первая Лига"), "Сб 04.05 18:00")
    expected_matches = {
        0: m1,
        1: m2
    }
    assert matches[0].date == expected_matches[0][0].date


@patch('src.requests_handler.requests.post')
def test_get_list_of_teams(mock_post):
    mock_post.return_value.json.return_value = mocked_response
    handler = Handler(data_1)
    teams = handler.get_list_of_teams()
    expected_teams = [Team("Машина", "Высшая Лига"), Team("Landragons", "Высшая Лига"),
                      Team("Аль-МФТИляль", "Высшая Лига"), Team("ИНБИКСТ", "Высшая Лига")]
    assert teams[0] == expected_teams[0]


@patch('src.requests_handler.requests.post')
def test_get_nearest_match(mock_post):
    mock_post.return_value.json.return_value = mocked_response
    with patch('src.requests_handler.compare_dates', return_value=True):
        date = get_nearest_match("Машина")
        assert date == "Пт 03.05 20:00"
    with patch('src.requests_handler.compare_dates', return_value=False):
        date = get_nearest_match("Машина")
        assert date == "расписания еще нет"
