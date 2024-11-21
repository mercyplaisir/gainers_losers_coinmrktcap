import pandas as pd
import json
import threading

import telebot.formatting
import func
import coinmktcap
import telegram
import time

import telebot
# from binance_handler.binance_handler.errors import SymbolNotFound

from binance_handler import order,binance_handler,errors



bot = telegram.get_bot()
def main():
    # get gainers and losers
    while True:
        count =1
        bulk_message = "" # append all message and send a bulk

        coinmktcap.run()
        print(f"checking...")
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


        # close by saving new data
        # coinmktcap.save_gainers_losers()
        if len(new_gainers_items)>0:
            for item in new_gainers_items:
                gainer_message = f"""NEW GAINER
                    Name : {item}
                    Volume  Mrktcap
                    {new_gainer.loc[item]['volume']}    {new_gainer.loc[item]['market_cap']}        
                    <a href = "{new_gainer.loc[item]['chart_link']}"> trdv link</a> & <a href = "https://www.binance.com/en/futures/{item}USDT"> binance </a>\n
                    Trend1h|Trend4h|trend1d
                    {new_gainer.loc[item]['trend_h1']}|{new_gainer.loc[item]['trend_h4']}|{new_gainer.loc[item]['trend_d1']}
                        """
                telegram.send_message(bot=bot,message=gainer_message)
                try:
                    order.market_buy_order(symbol=item+"USDT", quantity= binance_handler.minimum_notional(item+"USDT"))
                except errors.SymbolNotFound:
                    print(f"{item} was not found")
                
                
                # telegram.send_message(bot=bot,message=f"bought {item}")
                
                    

            
        if len(new_losers_items)>0:
            for item in new_losers_items:
                loser_message = f"""
                             NEW LOSER
                            Name : {item}
                            Volume | Mrktcap
                            {new_loser.loc[item]['volume']}  |  {new_loser.loc[item]['market_cap']}
                            <a href = "{new_loser.loc[item]['chart_link']}"> trdv </a> & <a href = "https://www.binance.com/en/futures/{item}USDT"> binance </a>
                            Trend1h|Trend4h|trend1d
                            {new_loser.loc[item]['trend_h1']}|{new_loser.loc[item]['trend_h4']}|{new_loser.loc[item]['trend_d1']}\n
                        """
                # telegram.send_channel_message(message)
                
                telegram.send_message(bot=bot,message=loser_message)
                
                try:
                    order.market_sell_order(item+"USDT", binance_handler.minimum_notional(item+"USDT")) #.minimum_quantity(item+"USDT"))
                # telegram.send_message(bot=bot,message=f"sold {item}")
                except errors.SymbolNotFound:
                    print(f"{item} was not found")
                    pass
        coinmktcap.save_gainers_losers()
        time.sleep(30)

def telegram_loop_running():
    telegram.infinity_polling(bot)


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=telegram_loop_running)

t1.start()
t2.start()

t1.join()
t2.join()