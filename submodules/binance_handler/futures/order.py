import datetime
import time
import requests
from ..funcs import funcs
from .binance_handler import _check_symbol
import submodules.binance_handler.errors.errors as bnbErrors


MAINLINK = " https://fapi.binance.com"

def now_timestamp():
    return int(round(time.time() * 1000))-2500

def binance_timestamp():  
    rs = requests.get(MAINLINK+"/fapi/v1/time")
    return rs.json()['serverTime']

def _order_check(rq:requests.Response) ->dict:
    if rq.json().get('orderId') is not None:
        return rq.json()
    raise bnbErrors.OrderNotSent

def _new_order(**kwargs) -> dict:# -> Any:
    lnk = MAINLINK + "/fapi/v1/order"
    rq = funcs.post_v3(lnk,**kwargs)
    print(rq.json(),f"\n{kwargs}___________")
    return _order_check(rq)

def _buy_order(**kwargs) ->dict:
    _check_symbol(kwargs["symbol"])
    data = {"side":"BUY","recvWindow": 5000,"timestamp": now_timestamp()}
    kwargs.update(data)
    return _new_order(**kwargs)
    
def _sell_order(**kwargs)->dict:
    _check_symbol(kwargs["symbol"])
    data = {"side":"SELL","recvWindow": 5000,"timestamp": now_timestamp()}
    kwargs.update(data)
    return _new_order(**kwargs)

def cancel_order(symbol,orderId):
    data = {"recvWindow": 5000,"timestamp": now_timestamp()}
    return _new_order(symbol = symbol,orderId = orderId,**data)
    ...

def market_sell_order(symbol:str,quantity:int|float )->dict:
    return _sell_order(symbol=symbol,quantity=quantity,type="MARKET")

def market_close_order(symbol:str,quantity:int|float,side:str )->dict:
    if side.upper() == "BUY":
        return market_buy_order(symbol=symbol,quantity=quantity)
    if side.upper() == "SELL":
        return market_sell_order(symbol=symbol,quantity=quantity)

def market_buy_order(symbol:str,quantity:int|float )->dict:
    return _buy_order(symbol=symbol,quantity=quantity,type="MARKET")


"""{
    "symbol":	STRING	YES
"side":	ENUM	YES
"positionSide":	ENUM	NO
"type":	ENUM	YES
"timeInForce":	ENUM	NO
"quantity":	DECIMAL	NO
"reduceOnly":	STRING	NO
"price":	DECIMAL	NO
"newClientOrderId":	STRING	NO
"stopPrice":	DECIMAL	NO
"closePosition":	STRING	NO
"activationPrice":	DECIMAL	NO
"callbackRate":	DECIMAL	NO
"workingType":	ENUM	NO
"priceProtect":	STRING	NO
"newOrderRespType":	ENUM	NO
"priceMatch":	ENUM	NO
"selfTradePreventionMode":	ENUM	NO
"goodTillDate":	LONG	NO
"recvWindow":	LONG	NO
"timestamp":	LONG	YES
}"""