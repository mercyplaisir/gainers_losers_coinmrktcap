import time
from func import _gainers,_losers
from binance_handler.futures.account_info import account_info_v3
from binance_handler.errors import errors
import telegram_handler
import telebot

bot = telegram_handler.get_bot()

GN_LOS_MESSAGE_ID = 1301
ACC_INFO_ID = 1300

def generate_gainers_losers_message():
    gainers=_gainers()
    losers = list(_losers())
    message=" \n|GAINERS| LOSERS|\n|_______|_______|\n"
    counter = 0
    for gainer in gainers:
        message+=f"| {gainer}{" "*(6-len(gainer))}|"
        while counter < len(losers):
            message+=f" {losers[counter]}{" "*(6-len(losers[counter]))}|"
            counter+=1
            break
        message+="\n"
    return message

def _get_account_info():
    try:
        data:dict = account_info_v3()
        return data
    except errors.TimestampOutofWindow:
        _get_account_info()

def generate_acc_info_message():
    data:dict = _get_account_info()
    _,_,walletBalance,unrealizedProfit,_,_,_,_,_,availableBalance,_,assets,positions = data.values()
    # print(walletBalance)
    message = f"BALANCE: {walletBalance} $\n"
    message+= f"UnrealisedProfit: {unrealizedProfit} $\n"
    message+= f"availableBAlance: {availableBalance} $\n"
    message += "Position:\n"
    position_counter=0
    if len(positions)>0:
        while position_counter<len(positions):
            # print(positions[position_counter])
            symbol,_,_,unrealized_profit,_,_,_,_,maintMargin,_ =  positions[position_counter].values()
            message+=f"{position_counter}.{symbol} | {maintMargin}$ | {unrealized_profit}$\n "
            position_counter += 1
    return message

def update_message():
    gain_los_message = generate_gainers_losers_message()
    gain_los_clean_message = telebot.formatting.hpre(gain_los_message)        
    acc_info_message = generate_acc_info_message()
    acc_info_clean_message = telebot.formatting.hpre(acc_info_message)
    try:    
        telegram_handler.update_channel_message(message_id=GN_LOS_MESSAGE_ID,bot=bot,message=gain_los_clean_message,parse_mode = "HTML")
        telegram_handler.update_channel_message(message_id=ACC_INFO_ID,bot=bot,message=acc_info_clean_message,parse_mode = "HTML")
    except telebot.apihelper.ApiTelegramException as e:
        print(e.description)
        print("trying in 30sec")
        time.sleep(30)



