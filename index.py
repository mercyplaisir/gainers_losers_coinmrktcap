import pandas as pd
import json
import threading
import func
import coinmktcap
import telegram
import time
bot = telegram.get_bot()
def main():
    # get gainers and losers
    while True:
        coinmktcap.run()
        print(f"checking...")
        # old
        old_gainer = func.load_data_json('./files/gainers.json')
        old_loser = func.load_data_json('./files/losers.json')
        
        old_gainers_index = func.index(old_gainer)
        old_losers_index = func.index(old_loser)

        # new
        new_gainer = func.load_data_json('./files/new_gainers.json')
        new_loser = func.load_data_json('./files/new_losers.json')
        
        new_gainers_index = func.index(new_gainer)
        new_losers_index =func.index( new_loser)

        new_gainers_items = func.list_comparison(old_gainers_index,new_gainers_index)
        new_losers_items = func.list_comparison(old_losers_index,new_losers_index)

        # close by saving new data
        # coinmktcap.save_gainers_losers()
        if len(new_gainers_items)>0:
            for item in new_gainers_items:
                message = f"""
                            \n\n  NEW GAINER
                                Name : {item}
                                Volume  Mrktcap
                                {new_gainer.loc[item]['volume']}    {new_gainer.loc[item]['market_cap']}            
                        """
                telegram.send_message(bot=bot,message=message)
        
            
        if len(new_losers_items)>0:
            for item in new_losers_items:
                message = f"""
                             NEW LOSER
                            Name : {item}
                            Volume | Mrktcap
                            {new_loser.loc[item]['volume']}  |  {new_loser.loc[item]['market_cap']}
                            trdv link
                            {new_loser.loc[item]['chart_link']}
                            Trend1h|Trend4h|trend1d
                            {new_loser.loc[item]['trend_h1']}|{new_loser.loc[item]['trend_h4']}|{new_loser.loc[item]['trend_d1']}
                        """
                telegram.send_message(bot=bot,message=message)
                # telegram.send_channel_message(message)


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