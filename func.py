from enum import Enum,auto
import time
import json
import requests
import pandas as pd

def save_rq(data,filepath=".",filename = "/rq"):
    with open(filepath+filename,'w') as f:
        f.write(data )
    return

def load_data_json(filepath) -> pd.DataFrame:
    with open(filepath,'r') as f:
        data = json.load(f)

    data = pd.DataFrame.from_dict(data)
    return data
def dump_data_json(filepath,data) -> None:
    
    with open(filepath,'w') as f:
        f.write(data)

def list_comparison(old:list,new:list):
    new_items = []
    for item in new:
        if item not in old:
            new_items.append(item)
    return new_items

index = lambda a : list(a.index)
# def index(a):
#     if a is not None:
#         return list(a.index)
#     else:
#         return []
def move_json(oldfile,newfile):
    d = load_data_json(oldfile).to_json()
    
    dump_data_json(newfile,d)

def request(rq):
    try:
        return requests.get(rq)
    except Exception as e :
        print(f"{__name__} - the error is",e)
        print(f"{__name__} - waiting 10second before retrying")
        time.sleep(10)
        request(e)


class Trend(Enum):
    UPTREND = auto()
    DOWNTREND = auto()
    
    def __str__(self) -> str:
        return f'{self.name}'
    def __eq__(self, __value: object) -> bool:
        return self.name ==  __value
    def __hash__(self) -> int:
        return hash(self.name)



def trend_calculator(df:pd.DataFrame) -> Trend:
        """give the trend of the current stock

        Args:
            df (pd.DataFrame): contains ohlc data of given crypto
        """
        # data
        
        sma_size = 200
        # Get the trend of the market by using sma200
        # Get list of 5 last closed price
        price: list[float] = df["close"][-5:].to_list()
        # calculate sma
        df[f"SMA_{sma_size}"] = df["close"].rolling(window=sma_size).mean()
        sma_value: list[float] = df[f"SMA_{sma_size}"][-5:].to_list()
        # condition
        cond = price > sma_value
        if cond:
            return Trend.UPTREND.name
        return Trend.DOWNTREND.name

TRADES = "files/trades.json"

def _save_order(order:dict):
    """{symbol,orderId,side,quantity}"""
    _old_data = _retrieve_orders()
    
    _old_data[order["symbol"]] = [order["side"],order["origQty"]]
    with open(TRADES,"w") as f:
        f.write(json.dumps(_old_data))

def _remove_orders(symbol):
    _old_data = _retrieve_orders()
    
    del _old_data[symbol]
    with open(TRADES,"w") as f:
        f.write(json.dumps(_old_data))

def _retrieve_orders() -> dict:
    with open(TRADES,'r+') as f:
        return json.load(f)

GAINERS = "files/gainers.json"
LOSERS = "files/losers.json"

def _gainers():
    with open(GAINERS,'r') as f:
        return json.load(f)['cmc_link'].keys()


def _losers():
    with open(LOSERS,'r') as f:
        return json.load(f)['cmc_link'].keys()



# print(f"{generate_gainers_message()}\n{generate_losers_message()}")


# print(_retrieve_orders())