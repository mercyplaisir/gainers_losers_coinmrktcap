"""

Contains handlers of the telegram button
"""
import os
import json
import time
from typing import Callable
from dotenv import load_dotenv,find_dotenv

from params import API_TOKEN, CHANNELID, CHATID
load_dotenv(find_dotenv())

import requests
from requests.exceptions import ReadTimeout
from requests.exceptions import Timeout
import telebot
import datetime




def get_bot() -> telebot.TeleBot:
    bot = telebot.TeleBot(API_TOKEN)
    return bot


# Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
def send_welcome(bot:telebot.TeleBot, message:str):
    return bot.send_message( chat_id=CHATID,text="""\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

def add_last_update_message(message:str):
    if "last update" not in message:
        # print("adding ...")
        message += "last update:{}".format(datetime.datetime.now())
        return message
    elif "last update"  in message:
        # print("updating ...")
        return update_last_update_message(message=message)

def update_last_update_message(message:str):
    # print(message)
    return add_last_update_message(message.split("last update")[0])

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
def echo_message(bot:telebot.TeleBot,message:str):
    bot.reply_to(message, message.text)



def send_channel_message(bot:telebot.TeleBot,message:str,**kwargs):
    message = add_last_update_message(message)
    try:
        return bot.send_message(chat_id=CHANNELID,text=message, timeout=30,**kwargs)#,link_preview_options={'is_disabled':False})
    except requests.exceptions.ConnectionError:
        print(f"{__name__} - connection error, trying in 30 sec")
        time.sleep(30)
        
        bot.send_message(chat_id=CHANNELID,text=message, timeout=30)#,link_preview_options={'is_disabled':False})

    except telebot.apihelper.ApiTelegramException as e:
        print(f"{__name__} - A request to the Telegram API was unsuccessful. Error code: 429. Description: Too Many Request")
        time.sleep(60)
        bot.send_message(chat_id=CHANNELID,text=message, timeout=30)#,link_preview_options={'is_disabled':False})
    except requests.exceptions.Timeout:
        print(f"{__name__} - experienced a timeout, waiting 60sec")
        time.sleep(60)
        bot.send_message(chat_id=CHANNELID,text=message, timeout=30)#,link_preview_options={'is_disabled':False})

def send_personal_message(bot:telebot.TeleBot,message:str,**kwargs):
    message = add_last_update_message(message)
    try:
        bot.send_message(chat_id=CHATID,text=message,timeout=30,**kwargs)
    except requests.exceptions.ConnectionError:
        print(f"{__name__} - connection error, trying in 30 sec")
        time.sleep(30)
        send_personal_message(bot,message)

def send_message(bot,message):
    send_channel_message(bot,message,parse_mode = 'HTML')

def update_personal_message(bot:telebot.TeleBot,message:str,message_id,**kwargs):
    message = add_last_update_message(message)
    try:
        bot.edit_message_text(chat_id=CHATID,text=message,message_id=message_id,timeout=30,**kwargs)
    except requests.exceptions.ConnectionError:
        print(f"{__name__} - connection error, trying in 30 sec")
        time.sleep(30)
        send_personal_message(bot,message)



def infinity_polling(bot:telebot.TeleBot) :
    
    try:
        bot.infinity_polling(timeout=50)
    except Timeout:
        print(f"{__name__} - Readtimout reaching telegram \n witing 10sec")
        time.sleep(10)
        infinity_polling(bot)
    except requests.ConnectionError:
        print(f"{__name__} - ConnectionError reaching telegram \n witing 10sec")
        time.sleep(10)
        infinity_polling(bot)


def update_channel_message(bot:telebot.TeleBot,message:str,message_id:int,**kwargs):
    message = add_last_update_message(message)
    try:
        return bot.edit_message_text(chat_id=CHANNELID,text=message, timeout=30,message_id=message_id,**kwargs)#,link_preview_options={'is_disabled':False})
    except requests.exceptions.ConnectionError:
        print(f"{__name__} - connection error, trying in 30 sec")
        time.sleep(30)
        bot.edit_message_text(chat_id=CHANNELID,text=message, timeout=30,message_id=message_id,**kwargs)#,link_preview_options={'is_disabled':False})

    except telebot.apihelper.ApiTelegramException as e:
        print(f"{__name__} - A request to the Telegram API was unsuccessful {e.description}")
        time.sleep(60)
        bot.edit_message_text(chat_id=CHANNELID,text=message, timeout=30,message_id=message_id,**kwargs)#,link_preview_options={'is_disabled':False})
    except requests.exceptions.Timeout:
        print(f"{__name__} - experienced a timeout, waiting 60sec")
        time.sleep(60)
        bot.edit_message_text(chat_id=CHANNELID,text=message, timeout=30,message_id=message_id,**kwargs)#,link_preview_options={'is_disabled':False})
