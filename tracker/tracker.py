from binance_handler.futures import errors
from coinmktcap import gainers_losers
import func 
import binance_handler.futures.order as bnb_order
import time

def printout(text:str):
    print(f"_______________\n{text}\n______________")

def track():
    time.sleep(60)
    while True:
        printout(f"{__name__} - tracking ...")
        gainers,losers  = gainers_losers()
        symbols_data = func._retrieve_orders()
        if len(symbols_data) == 0:
            pass
        symbols:list[str] = symbols_data.keys()

        for symbol in symbols:
            quote_symbol = symbol.replace("USDT","")
            if quote_symbol in gainers.keys() or quote_symbol in losers.keys():
                continue
            side,quantity=symbols_data[symbol]
            try:
                bnb_order.market_close_order(symbol=symbol,quantity=quantity,side=side_opposite(side))
                func._remove_orders(symbol=symbol)
                printout(f"{__name__}  - canceled {symbol} trade")
            except errors.OrderNotSent:
                printout(f"{__name__}  - order for {symbol}  not sent")
                pass
        time.sleep(70)
            

def side_opposite(side:str):
    if side.upper() == "BUY":
        return "SELL"
    if side.upper() == "SELL":
        return "BUY"
    


