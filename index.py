import pandas as pd
import json
import threading

import telebot

from binance_handler.futures import errors, order
import func
import coinmktcap
import messages
from order import send_buy_order, send_sell_order
import telegram
import time

from binance_handler.futures import binance_handler

from tracker import tracker

bot = telegram.get_bot()

GN_LOS_MESSAGE_ID = 1301






def main():
    # get gainers and losers
    while True:
        count =1
        bulk_message = "" # append all message and send a bulk

        coinmktcap.run()
        print(f"{__name__} - checking...")
        # old
        old_gainer = func.load_data_json('files/gainers.json')
        old_loser = func.load_data_json('files/losers.json')
        
        old_gainers_index = func.index(old_gainer)
        old_losers_index = func.index(old_loser)

        # new
        new_gainer = func.load_data_json('files/new_gainers.json')
        new_loser = func.load_data_json('files/new_losers.json')
        
        new_gainers_index = func.index(new_gainer)
        new_losers_index =func.index( new_loser)

        new_gainers_items = func.list_comparison(old_gainers_index,new_gainers_index)
        new_losers_items = func.list_comparison(old_losers_index,new_losers_index)

        coinmktcap.save_gainers_losers()
        TELEGRAM_UPDATE = False        
        if len(new_gainers_items)>0:
            for item in new_gainers_items:
                send_buy_order(item=item)
                TELEGRAM_UPDATE = True
        if len(new_losers_items)>0:
            for item in new_losers_items:
                send_sell_order(item=item)
                True
        
        if TELEGRAM_UPDATE:
            messages.update_message()
        time.sleep(30)

def telegram_loop_running():
    telegram.infinity_polling(bot)


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=telegram_loop_running)
t3 = threading.Thread(target=tracker.track)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()



