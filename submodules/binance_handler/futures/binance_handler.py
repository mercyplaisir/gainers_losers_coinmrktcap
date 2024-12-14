import requests
import json
from submodules.binance_handler.errors.errors import SymbolNotFound

FOLDER = "submodules/binance_handler/data"

RESTRUCTURED_DATA = FOLDER+"/restructured_data.json"
BINANCE_EXCHANGE_INFO = FOLDER+"/binance_exchange_info.json"

def exchange_information():
    main_lnk = "https://fapi.binance.com"
    lnk = main_lnk + "/fapi/v1/exchangeInfo"

    req = requests.get(lnk)
    # print(req.content)
    with open(BINANCE_EXCHANGE_INFO,"w") as f:
        f.write(json.dumps(req.json()))

def open_json(filepath):
    with open(filepath,'r') as f:
        d = json.load(f)
    return d

# exchange_information()

def pair_price(pair:str) -> float:
    main_lnk = "https://fapi.binance.com"
    lnk = main_lnk + "/fapi/v1/ticker/price"

    rq = requests.get(lnk,params={"symbol":pair})
    print(f"\n{__name__} price for  {pair} rq {rq.status_code} {rq.json()}\n")
    if rq.status_code == 400:
        raise SymbolNotFound()
    if not rq.json().get("price"):
        raise SymbolNotFound()
    return float(rq.json()["price"])

def future_symbols():
    data = open_json(BINANCE_EXCHANGE_INFO)
    symbols = [symbol_data['symbol'] for symbol_data in data['symbols']]
    return symbols
    ...

def symbol_price(symbol:str) -> float:
    main_lnk = "https://fapi.binance.com"
    lnk = main_lnk + "/fapi/v1/premiumIndex"

    rq = requests.get(lnk,params={"symbol":symbol})

    return float(rq.json()["markPrice"])


def minimum_notional(symbol:str) -> float:
    _check_symbol(symbol=symbol)
    data = open_json(RESTRUCTURED_DATA)
    
    new_data = float(data[symbol]['filters'][5]['notional'])
    return new_data *1.05 

def _verify_symbol(symbol):
    data:dict=open_json(RESTRUCTURED_DATA)
    symbols = data.keys()
    return  symbol in symbols

def _check_symbol(symbol) :   
    if not _verify_symbol(symbol):
        raise SymbolNotFound()
    
    
def _quantity_precision(symbol:str, amount:float|int)->float:
    _check_symbol(symbol=symbol)
    data = open_json(RESTRUCTURED_DATA)
    if type(amount) is int:
        return amount
    data[symbol]                # add a check symbol function
    return round(amount,data[symbol]['quantityPrecision'])
def minimum_quantity(symbol:str)-> float:
    _check_symbol(symbol=symbol)
    quantity = (minimum_notional(symbol=symbol)/symbol_price(symbol=symbol))*1.5
    return _quantity_precision(symbol,quantity)


# print(minimum_margin("BTCUSDT"))
# minimum_margin("BTCUSDT")
# exchange_information()