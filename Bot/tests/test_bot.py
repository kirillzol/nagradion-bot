import pytest
import os
from unittest.mock import patch, MagicMock
from src.bot import *


@pytest.fixture(scope="module")
def mock_subscriptions():
    subscriptions['123'] = ['Машина', 'Инбикст']
    yield
    subscriptions.clear()


def test_start_message(mock_subscriptions):
    with patch('telebot.TeleBot.send_message') as mock_send:
        message = MagicMock()
        message.chat.id = '123'
        start(message)
        assert mock_send.called
        called_args, called_kwargs = mock_send.call_args
        assert called_args[0] == '123'
        assert "Выберите одну из доступных опций" in called_kwargs['text']


def test_choose_league_message():
    with patch('telebot.TeleBot.send_message') as mock_send:
        message = MagicMock()
        message.chat.id = '123'
        choose_league(message)
        assert mock_send.called
        called_args, called_kwargs = mock_send.call_args
        assert called_args[0] == '123'
        assert "Выберите лигу" in called_kwargs['text']


def test_subscribe(mock_subscriptions):
    with patch('telebot.TeleBot.send_message') as mock_send:
        message = MagicMock()
        message.chat.id = '124'
        # subscribe(message, "AAA")
        subscribe(message, "Машина")
        assert mock_send.called
        called_args, called_kwargs = mock_send.call_args
        assert "Вы уже подписаны на уведомления о матчах команды Машина" in called_kwargs['text']


def test_unsubscribe(mock_subscriptions):
    with patch('telebot.TeleBot.send_message') as mock_send:
        message = MagicMock()
        message.chat.id = '123'
        unsubscribe(message, "Машина")
        assert mock_send.called
        called_args, called_kwargs = mock_send.call_args
        assert "Машина" not in subscriptions['123']
        unsubscribe(message, "Машина")


def test_save_subscriptions(mock_subscriptions):
    save_subscriptions()
    assert os.path.exists('subscriptions.json')
    with open('subscriptions.json', 'r') as f:
        data = json.load(f)
        assert '123' in data
        assert data['123'] == ['Инбикст']


def test_send_notifications(mock_subscriptions):
    with patch('telebot.TeleBot.send_message') as mock_send:
        send_notifications()
        assert mock_send.called
        called_args, called_kwargs = mock_send.call_args
        assert "Уведомление о матче команды" in called_kwargs['text']


def test_help_command():
    expected_response = (
        "/start - Запустить бота\n"
        "/help - Показать это сообщение\n"
        "Подписаться на матчи команды - Подписаться на уведомления о матчах команды\n"
        "Отписаться от уведомлений - Отписаться от уведомлений о матчах команды\n"
        "Увидеть подписки - Показать все ваши подписки\n"
        "Главное меню - Вернуться в главное меню"
    )
    assert help_command(None) == expected_response


