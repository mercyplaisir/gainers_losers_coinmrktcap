import threading

import func
import coinmktcap
import output.messages as messages
from order import  send_buy_order_notional, send_sell_order_notional
import telegram_handler
import time
from params import LEVERAGE, NOTIONAL, TELEGRAM_UPDATE

from tracker import tracker

bot = telegram_handler.get_bot()



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
               
        if len(new_gainers_items)>0:
            for item in new_gainers_items:
                send_buy_order_notional(item=item,notional=NOTIONAL,leverage_amount = LEVERAGE)
                TELEGRAM_UPDATE = True
        if len(new_losers_items)>0:
            for item in new_losers_items:
                send_sell_order_notional(item=item,notional=NOTIONAL, leverage_amount =LEVERAGE)
                True
        
        if TELEGRAM_UPDATE:
            messages.update_message()
        time.sleep(30)

def telegram_loop_running():
    telegram_handler.infinity_polling(bot)


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=telegram_loop_running)
t3 = threading.Thread(target=tracker.track)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()



