from func import _gainers,_losers
from binance_handler.futures.account_info import account_info_v3
import telegram
import telebot

bot = telegram.get_bot()

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


def generate_acc_info_message():

    _,_,walletBalance,unrealizedProfit,_,_,_,_,_,availableBalance,_,assets,positions = account_info_v3().values()
    print(walletBalance)
    message = f"BALANCE: {walletBalance} $\n"
    message+= f"UnrealisedProfit: {unrealizedProfit} $\n"
    message+= f"availableBAlance: {availableBalance} $\n"
    message += "Position:\n"
    position_counter=0
    if len(positions)>0:
        while position_counter<len(positions):
            print(positions[position_counter])
            symbol,_,_,unrealized_profit,_,_,_,_,maintMargin,_ =  positions[position_counter].values()
            message+=f"{symbol} - {maintMargin}$ - {unrealized_profit}$\n "
            position_counter += 1
            break

    return message

    


def update_message():
    gain_los_message = generate_gainers_losers_message()
    gain_los_clean_message = telebot.formatting.hpre(gain_los_message)    
    
    acc_info_message = generate_acc_info_message()
    acc_info_clean_message = telebot.formatting.hpre(acc_info_message)    

    telegram.update_channel_message(message_id=GN_LOS_MESSAGE_ID,bot=bot,message=gain_los_clean_message,parse_mode = "HTML")
    telegram.update_channel_message(message_id=ACC_INFO_ID,bot=bot,message=acc_info_clean_message,parse_mode = "HTML")
