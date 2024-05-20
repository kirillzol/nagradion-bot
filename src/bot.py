import telebot
from telebot import types
import schedule
import time
import asyncio
import threading
from src.requests_handler import *
import json
import os

list_of_teams = Handler(data_1).get_list_of_teams() + Handler(data_2).get_list_of_teams() + Handler(
    data_3).get_list_of_teams()

key = os.environ.get('TOKEN')
bot = telebot.TeleBot(key)

subscriptions = {}

flag = True

try:
    with open('subscriptions.json', 'r') as f:
        subscriptions = json.load(f)
except FileNotFoundError:
    subscriptions = {}


def save_subscriptions():
    with open('subscriptions.json', 'w') as f:
        json.dump(subscriptions, f)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Подписаться на матчи команды")
    btn2 = types.KeyboardButton("Отписаться от уведомлений")
    btn3 = types.KeyboardButton("Увидеть подписки")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Выберите одну из доступных опций".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    if message and hasattr(message, 'chat'):
        chat_id = message.chat.id
        response = (
            "/start - Запустить бота\n"
            "/help - Показать это сообщение\n"
            "Подписаться на матчи команды - Подписаться на уведомления о матчах команды\n"
            "Отписаться от уведомлений - Отписаться от уведомлений о матчах команды\n"
            "Увидеть подписки - Показать все ваши подписки\n"
            "Главное меню - Вернуться в главное меню"
        )
        bot.send_message(chat_id, response)
        return response
    else:
        return (
            "/start - Запустить бота\n"
            "/help - Показать это сообщение\n"
            "Подписаться на матчи команды - Подписаться на уведомления о матчах команды\n"
            "Отписаться от уведомлений - Отписаться от уведомлений о матчах команды\n"
            "Увидеть подписки - Показать все ваши подписки\n"
            "Главное меню - Вернуться в главное меню"
        )
def choose_league(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вторая Лига")
    btn2 = types.KeyboardButton("Первая Лига")
    btn3 = types.KeyboardButton("Высшая Лига")
    btn4 = types.KeyboardButton("Главное меню")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Выберите лигу", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global flag
    user_id = str(message.chat.id)
    text = message.text

    if text == "Подписаться на матчи команды":
        flag = False
        choose_league(message)
    elif text in ["Вторая Лига", "Первая Лига", "Высшая Лига"]:
        show_teams(message, text)
    elif text == "Главное меню":
        start(message)
    elif text == "Увидеть подписки":
        show_subscriptions(message)
    elif text == "Отписаться от уведомлений":
        flag = True
        show_subscriptions_to_be_deleted(message)
    elif text in list_of_teams and flag == False:
        subscribe(message, text)
    elif text in list_of_teams and flag == True:
        unsubscribe(message, text)


def show_teams(message, league):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    handler = Handler(data_1 if league == "Высшая Лига" else data_2 if league == "Первая Лига" else data_3)
    teams = handler.get_list_of_teams()
    for team in teams:
        btn = types.KeyboardButton(team.name)
        markup.add(btn)
    btn_main = types.KeyboardButton("Главное меню")
    markup.add(btn_main)
    bot.send_message(message.chat.id, text="Выберите команду для подписки", reply_markup=markup)


def show_subscriptions_to_be_deleted(message):
    user_id = str(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for team in subscriptions[user_id]:
        btn = types.KeyboardButton(team)
        markup.add(btn)
    btn_main_menu = types.KeyboardButton("Главное меню")
    markup.add(btn_main_menu)
    bot.send_message(message.chat.id, text="Выберете команду, от уведомлений о матчах которой вы хотите отписаться",
                     reply_markup=markup)


def subscribe(message, team_name):
    user_id = str(message.chat.id)
    if user_id not in subscriptions:
        subscriptions[user_id] = []
    if team_name not in subscriptions[user_id]:
        subscriptions[user_id].append(team_name)
        bot.send_message(message.chat.id, text=f"Вы подписались на уведомления о матчах команды {team_name}")
    else:
        bot.send_message(message.chat.id, text=f"Вы уже подписаны на уведомления о матчах команды {team_name}")


def unsubscribe(message, team_name):
    user_id = str(message.chat.id)
    if team_name not in subscriptions[user_id]:
        bot.send_message(message.chat.id,
                         text=f"Вы не подписаны на уведомлений о матчах команды {message.text}")
        start(message)
    else:
        subscriptions[user_id].remove(team_name)
        save_subscriptions()
        bot.send_message(message.chat.id, text=f"Вы отписались от уведомлений о матчах команды {message.text}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for team in subscriptions[user_id]:
            btn = types.KeyboardButton(team)
            markup.add(btn)
        btn_main_menu = types.KeyboardButton("Главное меню")
        markup.add(btn_main_menu)


def show_subscriptions(message):
    user_id = str(message.chat.id)
    if user_id in subscriptions and subscriptions[user_id]:
        text = "Ваши подписки:\n" + "\n".join(subscriptions[user_id])
    else:
        text = "У вас нет подписок"
    bot.send_message(message.chat.id, text=text)


async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def send_notifications():
    for user_id, teams in subscriptions.items():
        for team in teams:
            bot.send_message(user_id, text=f"Уведомление о матче команды {team}")

schedule.every().day.at("10:00").do(send_notifications)

def run_bot():
    bot.polling(none_stop=True)

