from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
import requests
import hmac
import base64
import hashlib
import submodules.binance_handler.errors.errors as errors

import os


PUBLICKEY = os.getenv('PUBLICKEY')
SECRETKEY = os.getenv('SECRETKEY')

def _add_signature(message:str,key:str=SECRETKEY):
    # print(SECRETKEY)
    h = hmac.new(key=key.encode(),msg=message.encode(),digestmod=hashlib.sha256)
    return h.hexdigest()

def _dict_to_str(kwargs:dict,sign:bool=False):
    msg = ""
    for key in  kwargs.keys():
        msg+= f"{key}="+f"{kwargs[key]}&"
    msg=msg[:-1]
    if sign:
        return _add_signature(msg)
    return msg

def _error_check(rq:requests.Response) -> requests.Response:
    if rq.json().get('code'):
        print(rq.json())
        raise errors.get_error(rq.json()['code'])
    return rq

def _params_v3(**kwargs):# -> dict[str, Any]:
    kwargs["signature"] = _dict_to_str(kwargs,True)
    return kwargs

def get_v3(url,**params) -> requests.Response:
    params = _params_v3(**params)
    rq = requests.get(url=url,params=params,headers={"X-MBX-APIKEY":PUBLICKEY})
    return _error_check(rq)
def post_v3(url,**params) -> requests.Response:
    params = _params_v3(**params)
    rq = requests.post(url=url,params=params,headers={"X-MBX-APIKEY":PUBLICKEY})
    return _error_check(rq)
