from binance_handler.errors import errors
from coinmktcap import gainers_losers
import func 
import binance_handler.futures.order as bnb_order
import time
import output.messages as messages

def printout(text:str):
    print(f"\n_______________\n{text}\n______________\n")

def track():
    time.sleep(60)
    while True:
        printout(f"{__name__} - tracking ...")
        gainers,losers  = gainers_losers()
        symbols_data = func._retrieve_orders()
        if len(symbols_data) == 0:
            continue
        symbols:list[str] = symbols_data.keys()

        for symbol in symbols:
            quote_symbol = symbol.replace("USDT","")
            if quote_symbol in gainers.keys() or quote_symbol in losers.keys():
                continue
            side,quantity=symbols_data[symbol]
            
            closeorder(symbol=symbol,quantity=quantity,side=side_opposite(side))
            
        time.sleep(70)

def closeorder(symbol,quantity,side):
    try:
        r = bnb_order.market_close_order(symbol=symbol,quantity=quantity,side=side)
        func._remove_orders(symbol=symbol)
        printout(f"{__name__}  - canceled {symbol} trade")
    except errors.OrderNotSent:
        printout(f"{__name__}  - order for {symbol}  not sent\n trying again")
        closeorder(symbol,quantity,side)
        pass
    except errors.TimestampOutofWindow:
        printout(f"{__name__}  - order for {symbol}  not sent Ttimestamp out of window\n trying again")
        closeorder(symbol,quantity,side)
        pass


def side_opposite(side:str):
    if side.upper() == "BUY":
        return "SELL"
    if side.upper() == "SELL":
        return "BUY"
    

