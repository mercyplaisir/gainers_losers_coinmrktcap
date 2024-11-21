import func
import pandas as pd
import requests
import urllib3
import time

def klines_future(pair:str,interval:str='5m'):
    
    try:
        rs = requests.get("https://fapi.binance.com/fapi/v1/indexPriceKlines",params={
            "pair": pair,
            "contractType": "PERPERTUAL",
            "interval" : interval
        })
    except urllib3.exceptions.TimeoutError:
        print("problem with connecting to binance, lets wait 1min")
        time.sleep(60)
        klines_future(pair,interval)
    except requests.exceptions.ConnectionError:
        print("Connection aborted.', waiting 60sec")
        time.sleep(60)
        klines_future(pair,interval)
    df = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
    df = df.get(["open time","open","high","low","close","close time"])
    df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
    # df = df.set_index([pd.Index([i for i in range(df.shape[0])]),'open time'])
    # print(df)
    return df
 
# print(klines_future('BTCUSDT'))