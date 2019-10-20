import telebot
from telebot.types import Message
from flask import Flask, request
import BotApi as bt
import requests


url_bot = bt.telegramBotApiUrl
token_bot=bt.telegramBotToken
money=bt.url_current
weather=bt.ApiUrlWeather
bot=telebot.TeleBot(token_bot)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(m:Message):
    bot.send_message(m.chat.id,'Привет!')

@bot.message_handler(commands=['help'])
def help(m:Message):
    bot.send_message(m.chat.id, 'Меня зовут Jonny, '
                                'я вывожу курсы валют и погоду, '
                                'но пока не допилил разработчик)')

def get_current(cur='USD'):
    res=requests.get(money)
    res_current=res.json()[0]

    current_in=res_current['{}_in'.format(cur)]
    current_out=res_current['{}_out'.format(cur)]

    return 'Продажа {} --> покупка {}'.format(current_out, current_in)
    pass

@bot.message_handler(commands=['current'])
def choice_course(m:Message):
    bot.send_message(m.chat.id, "Какую валюту вывести?")

    @bot.message_handler(content_types=['text'])
    def current(m:Message):
        try:
            bot.send_message(m.chat.id, get_current(str(m.text).upper()))
        except:
            bot.send_message(m.chat.id, 'Такой валюты нет! \n Введи валюту на английском языке (usd/USD)')


@bot.message_handler(commands=['weather'])
def choice_weather(m:Message):
    bot.send_message(m.chat.id, "Погоду какого города и страны вывести?")

    def get_weather(city):
        try:
            res=requests.get(weather.format(city))
        except:
            bot.send_message(m.chat.id, str(res.json()['cod']))

        result_weather=res.json()

        name = result_weather['list'][0]['name']
        conditions = result_weather['list'][0]['weather'][0]['description']
        temp = result_weather['list'][0]['main']['temp'] - 273.15
        return 'Город: {}, температура: {} °C, {}'.format(name, '%.1f' %temp, conditions)
        pass

    @bot.message_handler(content_types=['text'])
    def conclusion_weather(m:Message):
        try:
            bot.send_message(m.chat.id, get_weather(str(m.text)))
        except:
            bot.send_message(m.chat.id, "Ты не правильно указал"
                                        " город и страну (Brest, by)")

bot.polling()
