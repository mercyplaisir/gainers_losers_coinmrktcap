import func
import pandas as pd
import requests
def klines_future(pair:str,interval:str='5m'):
    rs = requests.get("https://fapi.binance.com/fapi/v1/indexPriceKlines",params={
        "pair": pair,
        "contractType": "PERPERTUAL",
        "interval" : interval
    })
    df = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
    df = df.get(["open time","open","high","low","close","close time"])
    df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
    # df = df.set_index([pd.Index([i for i in range(df.shape[0])]),'open time'])
    # print(df)
    return df

# print(klines_future('BTCUSDT'))