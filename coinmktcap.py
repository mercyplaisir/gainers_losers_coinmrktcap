from typing import List
from func import save_soup
from threading import Thread
# from tradeapp.exchanges.binancef.models.timeframe import Timeframe
# from tradeapp.exchanges.binancef.models.trend import Trend
import requests
from bs4 import BeautifulSoup

import pandas as pd

from enum import Enum,auto

class Trend(Enum):
    UPTREND = auto()
    DOWNTREND = auto()
    
    def __str__(self) -> str:
        return f'{self.name}'
    def __eq__(self, __value: object) -> bool:
        return self.name ==  __value
    def __hash__(self) -> int:
        return hash(self.name)


class Timeframe(Enum):
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    DAY = '1d'
    WEEK = '1w'

    def __repr__(self) -> str:
        return  f'{self.value}'

    def __str__(self) -> str:
        return  f'{self.value}'
    def __eq__(self, __value: object) -> bool:
        return self.value==__value
    def __hash__(self) -> int:
        return hash(self.value)
# from tradeapp.exchanges.binancef.models.trend import Trend

# from tradeapp.exchanges.binancef.binanceFuture import (
#     binance_future,
#     get_bal_of,
#     market_buy_order,
#     klines_future,
#     last_price,
#     market_sell_order
# )

link = "https://fr.tradingview.com/chart/?symbol=BINANCE%3A{}"

def get_cmc_link():
    ...
def get_tradingview_link(coin:str):
    link = "https://fr.tradingview.com/chart/?symbol=BINANCE%3A{}usdt"
    return link.format(coin)
# @logger_wrapper(__name__,"retreiving klines")
def klines_future(pair:str,interval:str):
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

def trend_calculator(df:pd.DataFrame) -> Trend:
        """give the trend of the current stock

        Args:
            df (pd.DataFrame): contains ohlc data of given crypto
        """
        # data
        
        sma_size = 200
        # Get the trend of the market by using sma200
        # Get list of 5 last closed price
        price: List[float] = df["close"][-5:].to_list()
        # calculate sma
        df[f"SMA_{sma_size}"] = df["close"].rolling(window=sma_size).mean()
        sma_value: List[float] = df[f"SMA_{sma_size}"][-5:].to_list()
        # condition
        cond = price > sma_value
        if cond:
            return Trend.UPTREND
        return Trend.DOWNTREND

# print(gainers_losers())

def trend(crypto,timeframe):
    klines = klines_future(crypto,timeframe)
    return trend_calculator(klines)
def gainers_losers():
    # Get trending coins
    main_lnk = "https://coinmarketcap.com"
    lnk = main_lnk + "/gainers-losers"

    req = requests.get(lnk)
    soup = BeautifulSoup(req.text,features="html.parser")

    gainers_table,losers_table = soup.find_all('table')
    # tds:list = gainers_table.find_all('p',{'class':'sc-4984dd93-0 kKpPOn'})
    gainers_name = gainers_table.find_all('p',{'class':'sc-71024e3e-0 OqPKt coin-item-symbol'})
    gainers_volume_tr = gainers_table.find_all('tr')
    # print(gainers_volume_tr[1].fin)
    gainers_volume = [tr.find_all('td')[4].text for tr in gainers_volume_tr[1:]]

    gainers_cmc_link = [ main_lnk + tr.find_all('td')[1].a.get('href')
                         for tr in gainers_volume_tr[1:]]

    gainers_change = [tr.find_all('td')[3].text for tr in gainers_volume_tr[1:]]
    # print(gainers_volume_tr_td)
    losers_name = losers_table.find_all('p',{'class':'sc-71024e3e-0 OqPKt coin-item-symbol'})
    losers_volume_tr = losers_table.find_all('tr')
    # print(gainers_volume_tr[1].fin)
    losers_volume = [tr.find_all('td')[4].text for tr in losers_volume_tr[1:]]
    losers_cmc_link = [ main_lnk + tr.find_all('td')[1].a.get('href')
                         for tr in losers_volume_tr[1:]]
    losers_change = [tr.find_all('td')[3].text for tr in losers_volume_tr[1:]]

    # print(losers_volume_tr_td)
    # data ={
    #     'gainers':[p.text+'USDT' for p in gainers],
                    
    #     'losers':[p.text+'USDT' for p in losers]
    # }
    
    gainers = {
        'crypto' : [p.text for p in gainers_name],
        # 'volume' : [vol for vol in gainers_volume],
        # 'change' : [ch for ch in gainers_change],
        'chart_link' : [link.format(p.text+"USDT") for p in gainers_name],
        'cmc_link' : [link for link in gainers_cmc_link],
    }
    
    losers ={
        'crypto' : [p.text for p in losers_name],
        # 'volume' : [vol for vol in losers_volume],
        'change' : [ch for ch in losers_change],
        'chart_link' : [link.format(p.text+"USDT") for p in losers_name],
        'cmc_link' : [link for link in losers_cmc_link],
    }
    return gainers,losers

def get_cmc_soup(cmc_link):
    req = requests.get(cmc_link)
    soup = BeautifulSoup(req.text,features="html.parser")
    return soup
def clean_crypto_data(crypto_data):
    mrkt_cap,volume,fdv,vol_mrkt_cap = crypto_data[:4]
    print(mrkt_cap.text,volume.text,fdv.text,vol_mrkt_cap.text)
    if 'B' in str(mrkt_cap.text) :
        mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('B') 
        mrkt_cap+='B'
    elif 'T' in str(mrkt_cap.text):
        mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('T')
        mrkt_cap+='T'
    else :
        mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('M')
        mrkt_cap+='M'
       # checking Volume 
    if 'B' in str(volume.text) :
        vol,vol_perc = str(volume.text).split('B')
        vol+='B'
    else:
        vol,vol_perc = str(volume.text).split('M')
        vol+='M'
    return [mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv.text,vol_mrkt_cap.text]

def get_crypto_data(cmc_link:str):
    
    soup = get_cmc_soup(cmc_link)

    # tbl = soup.find_all('div',{'class': 'sc-f70bb44c-0 iQEJet'})
    # save_soup(req.text)
    crypto_data = soup.find_all('dd',{'class':'sc-65e7f566-0 eQBACe StatsInfoBox_content-wrapper__onk_o'})
    mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv,vol_mrkt_cap = clean_crypto_data(crypto_data)

    return mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv,vol_mrkt_cap

gainers,losers = gainers_losers()

#gainers['volume'] = []
gainers['market_cap'] = []
gainers['markt_cap_perc']=[]
gainers['volume']=[]
gainers['vol_perc']=[]
gainers['fdv']=[]
gainers['vol/mrktcap'] = []

losers['market_cap'] = []
losers['markt_cap_perc']=[]
losers['volume']=[]
losers['vol_perc']=[]
losers['fdv']=[]
losers['vol/mrktcap'] = []

# ------------
def append_gainer(cmclink):
    mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv,vol_mrkt_cap = get_crypto_data(cmclink)
    gainers['market_cap'].append(mrkt_cap)
    gainers['markt_cap_perc'].append(mrkt_cap_perc)
    gainers['volume'].append(vol)
    gainers['vol_perc'].append(vol_perc)
    gainers['vol/mrktcap'].append(vol_mrkt_cap)
    gainers['fdv'].append(fdv)

threads = []
for link in gainers['cmc_link']:
    thread = Thread(target=append_gainer,kwargs={'cmclink':link})
    threads.append(thread)  
    thread.start()


# gainers['trend_d1'] = [trend(p+'USDT',Timeframe.DAY) for p in gainers['crypto']]
# gainers['trend_h4'] = [trend(p+'USDT',Timeframe.H4) for p in gainers['crypto']]
# gainers['trend_h1'] = [trend(p+'USDT',Timeframe.H1) for p in gainers['crypto']]
# losers['trend_d1'] = [trend(p+'USDT',Timeframe.DAY) for p in losers['crypto']]
# losers['trend_h4'] = [trend(p+'USDT',Timeframe.H4) for p in losers['crypto']]
# losers['trend_h1'] = [trend(p+'USDT',Timeframe.H1) for p in losers['crypto']]

#for gainers
# print(df_gainers_transposed)
#for losers
print("finish gainers")
def append_loser(cmclink):
    mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv,vol_mrkt_cap = get_crypto_data(cmclink)
    losers['market_cap'].append(mrkt_cap)
    losers['markt_cap_perc'].append(mrkt_cap_perc)
    losers['volume'].append(vol)
    losers['vol_perc'].append(vol_perc)
    losers['vol/mrktcap'].append(vol_mrkt_cap)
    losers['fdv'].append(fdv)
losers_threads=[]
for link in losers['cmc_link']:
    thread = Thread(target=append_loser,kwargs={'cmclink':link})
    threads.append(thread)  
    thread.start()

for thr in threads:
    thr.join()


df_gainers = pd.DataFrame.from_dict(gainers,orient='index')
df_gainers = df_gainers.transpose()
df_gainers.to_excel('gainers.xlsx')
df_losers = pd.DataFrame.from_dict(losers,orient='index')
df_losers = df_losers.transpose()
df_losers.to_excel('losers.xlsx')

def get_gainers():
    return df_gainers
def get_losers():
    return df_losers 