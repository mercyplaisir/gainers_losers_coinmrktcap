"""

Contains handlers of the telegram button
"""
import os
import json
import time
from typing import Callable
from dotenv import load_dotenv,find_dotenv

import requests
from requests.exceptions import ReadTimeout
from requests.exceptions import Timeout
import telebot


load_dotenv(find_dotenv())
API_TOKEN = os.getenv('TELEGRAM')

CHATID = os.getenv('CHATID')
CHANNELID= os.getenv('CHANNELID')

bot = telebot.TeleBot(API_TOKEN)


def get_bot():
    return bot


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

def send_message(bot:telebot.TeleBot,message):
    bot.send_message(chat_id=CHATID,text=message)
def send_channel_message(bot:telebot.TeleBot,message):
    bot.send_message(chat_id=CHANNELID,text=message)

def infinity_polling(bot:telebot.TeleBot):
    while True:
        try:
            bot.polling(timeout=30)
        except Timeout:
            print("Readtimout reaching telegram \n witing 10sec")
            time.sleep(10)
        


# send_message('hello')

# def send_new_items:


# bot.infinity_polling()