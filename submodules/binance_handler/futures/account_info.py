import requests
import time
from submodules.binance_handler.funcs import funcs
MAIN_LINK = "https://fapi.binance.com"

def now_timestamp():
    return int(round(time.time() * 1000))-2500

def _get_req(url,**kwargs):
    return requests.get(url,params=kwargs)

def _get_req_v3(url):
    ...
    


def account_info_v3()->dict:
    LNK = MAIN_LINK + "/fapi/v3/account"
    kwargs={"recvWindow": 5000,"timestamp": now_timestamp()}
    print(f"{__name__} -- {kwargs}")
    rq = funcs.get_v3(LNK,**kwargs)
    return rq.json()




