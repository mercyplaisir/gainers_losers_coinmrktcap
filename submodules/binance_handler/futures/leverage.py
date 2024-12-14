import datetime
import hashlib
import hmac
import time
import requests
from submodules.binance_handler.funcs import funcs

MAINLINK = " https://fapi.binance.com"




def now_timestamp():
    return int(round(time.time() * 1000))-2500

def leverage(symbol:str,leverage:int):
    lnk = MAINLINK+"/fapi/v1/leverage"
    params = {"symbol":symbol,"leverage":leverage,"recvWindow": 5000,"timestamp": now_timestamp()}
    # params = funcs._params_v3(symbol=symbol,leverage=leverage,recvWindow= 5000,timestamp= now_timestamp())
    # rq =  requests.post(url=lnk,params = params)
    # rq =  requests.post(url=lnk,params = params)
    print(params)
    rq = funcs.post_v3(lnk,**params)
    


