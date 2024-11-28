from typing import List
import binance
import func
from threading import Thread
import os
# from tradeapp.exchanges.binancef.models.timeframe import Timeframe
# from tradeapp.exchanges.binancef.models.trend import Trend
import requests
from bs4 import BeautifulSoup

import pandas as pd

from enum import Enum,auto
import time

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

def get_gainlos_page():
    main_lnk = "https://coinmarketcap.com"
    lnk = main_lnk + "/gainers-losers"
    try:
        rq = requests.get(lnk)
    except requests.exceptions.ConnectionError:
        print(f"{__name__} - max retries reachedstoping for a min")
        time.sleep(60)
        get_gainlos_page()
    return rq

def get_coin_page(lnk):
    try:
        rq = requests.get(lnk)
    except requests.exceptions.ConnectionError:
        print(f"{__name__} - max retries reachedstoping for a min")
        time.sleep(60)
        get_coin_page()
    return rq


def get_tradingview_link(coin:str):
    link = "https://fr.tradingview.com/chart/?symbol=BINANCE%3A{}usdt"
    return link.format(coin)
# @logger_wrapper(__name__,"retreiving klines")




# print(gainers_losers())

def trend(crypto,timeframe):
    klines = binance.klines_future(crypto,timeframe)
    return func.trend_calculator(klines)


def gainers_losers():
    """_summary_

    Returns:
        _type_: {crypto:
        { chart_link: ...,
        cmc_link:...,
        market_cap:...,
        markt_cap_perc:...,
        volume:...,
        vol_perc:...,
        fdv:...,
        vol/mrktcap:...
        }}
    """
    # Get trending coins
    main_lnk = "https://coinmarketcap.com"
    # lnk = main_lnk + "/gainers-losers"

    # req = func.request(lnk)
    req = get_gainlos_page()
    soup = BeautifulSoup(req.text,features="html.parser")

    gainers_table,losers_table = soup.find_all('table')
    # tds:list = gainers_table.find_all('p',{'class':'sc-4984dd93-0 kKpPOn'})
    gainers_name = gainers_table.find_all('p',{'class':'sc-71024e3e-0 OqPKt coin-item-symbol'})
    gainers_volume_tr = gainers_table.find_all('tr')
    # print(gainers_volume_tr[1].fin)
    # gainers_volume = [tr.find_all('td')[4].text for tr in gainers_volume_tr[1:]]

    gainers_cmc_link = [ main_lnk + tr.find_all('td')[1].a.get('href')
                         for tr in gainers_volume_tr[1:]]

    # gainers_change = [tr.find_all('td')[3].text for tr in gainers_volume_tr[1:]]
    # print(gainers_volume_tr_td)
    losers_name = losers_table.find_all('p',{'class':'sc-71024e3e-0 OqPKt coin-item-symbol'})
    losers_volume_tr = losers_table.find_all('tr')
    # print(gainers_volume_tr[1].fin)
    # losers_volume = [tr.find_all('td')[4].text for tr in losers_volume_tr[1:]]
    losers_cmc_link = [ main_lnk + tr.find_all('td')[1].a.get('href')
                         for tr in losers_volume_tr[1:]]
    # losers_change = [tr.find_all('td')[3].text for tr in losers_volume_tr[1:]]
    
    gainers = {
        'crypto' : [p.text for p in gainers_name],
        # 'volume' : [vol for vol in gainers_volume],
        # 'change' : [ch for ch in gainers_change],
        'chart_link' : [link.format(p.text+"USDT") for p in gainers_name],
        'cmc_link' : [link for link in gainers_cmc_link],
    }
    """{name:{}}
        { chart_link: ...,
        cmc_link:...,
        market_cap:...,
        markt_cap_perc:...,
        volume:...,
        vol_perc:...,
        fdv:...,
        vol/mrktcap:...
        }}"""
    gainers={}
    counter = 0
    for name in gainers_name:
        gainers[name.text]={ 'chart_link': link.format(name.text+"USDT"),
        'cmc_link':gainers_cmc_link[counter],}
        counter+=1
    
    # losers ={
    #     'crypto' : [p.text for p in losers_name],
    #     # 'volume' : [vol for vol in losers_volume],
    #     'change' : [ch for ch in losers_change],
    #     'chart_link' : [link.format(p.text+"USDT") for p in losers_name],
    #     'cmc_link' : [link for link in losers_cmc_link],
    # }
    losers={}
    counter = 0
    for name in losers_name:
        losers[name.text]={ 'chart_link': link.format(name.text+"USDT"),
        'cmc_link':losers_cmc_link[counter],}
        counter+=1
    return gainers,losers

def get_soup(req):
    soup = BeautifulSoup(req.text,features="html.parser")
    return soup



def save_soup(soup:BeautifulSoup):
    with open('test.html','w+') as f:
        f.write(soup.decode())

def clean_crypto_data(crypto_data):
    try:
        mrkt_cap,volume,fdv,vol_mrkt_cap = crypto_data[:4]
        # print(mrkt_cap.text,volume.text,fdv.text,vol_mrkt_cap.text)
        if 'B' in str(mrkt_cap.text) :
            mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('B') 
            mrkt_cap+='B'
        elif 'T' in str(mrkt_cap.text):
            mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('T')
            mrkt_cap+='T'
        elif 'K' in str(mrkt_cap.text):
            mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('K')
            mrkt_cap+='K'
        else :
            mrkt_cap,mrkt_cap_perc = str(mrkt_cap.text).split('M')
            mrkt_cap+='M'
        # checking Volume 
        if 'B' in str(volume.text) :
            vol,vol_perc = str(volume.text).split('B')
            vol+='B'
        elif 'K' in str(volume.text):
            vol,vol_perc = str(volume.text).split('K')
            vol+='K'
        elif 'T' in str(volume.text):
            vol,vol_perc = str(volume.text).split('T')
            vol+='T'
        else:
            vol,vol_perc = str(volume.text).split('M')
            vol+='M'
        return [mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv.text,vol_mrkt_cap.text]
    except:
        print(crypto_data)


def get_crypto_data(soup):
    crypto_data = soup.find_all('dd',{'class':'sc-65e7f566-0 eQBACe StatsInfoBox_content-wrapper__onk_o'})
    # print(crypto_data)
    return crypto_data




def append_loser(losers):
    threads = []
    def _thread_way(losers:dict,loser:str):
        # print(f"{__name__} - getting for {loser}")
        rq:requests.Response = get_coin_page(losers[loser]["cmc_link"])
        soup: BeautifulSoup = get_soup(rq)
        mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv,vol_mrkt_cap = clean_crypto_data(get_crypto_data(soup))
        losers[loser]['market_cap']=mrkt_cap
        losers[loser]['markt_cap_perc']=mrkt_cap_perc
        losers[loser]['volume']=vol
        losers[loser]['vol_perc']=vol_perc
        losers[loser]['vol/mrktcap']=vol_mrkt_cap
        losers[loser]['fdv']=fdv
        losers[loser]['trend_d1'] = trend(loser+'USDT',Timeframe.DAY)
        losers[loser]['trend_h4'] = trend(loser+'USDT',Timeframe.H4) 
        losers[loser]['trend_h1'] = trend(loser+'USDT',Timeframe.H1) 
    for loser in losers.keys():
        thread = Thread(target=_thread_way,kwargs={'losers':losers,'loser':loser})
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def append_gainer(gainers:dict):
    threads = []
    def _thread_way(gainers:dict,gainer:str):
        # print(f"{__name__} - getting for {gainer}")
        rq:requests.Response = get_coin_page(gainers[gainer]["cmc_link"])
        soup: BeautifulSoup = get_soup(rq)
        mrkt_cap,mrkt_cap_perc,vol,vol_perc,fdv,vol_mrkt_cap = clean_crypto_data(get_crypto_data(soup))
        gainers[gainer]['market_cap']=mrkt_cap
        gainers[gainer]['markt_cap_perc']=mrkt_cap_perc
        gainers[gainer]['volume']=vol
        gainers[gainer]['vol_perc']=vol_perc
        gainers[gainer]['vol/mrktcap']=vol_mrkt_cap
        gainers[gainer]['fdv']=fdv
        gainers[gainer]['trend_d1'] = trend(gainer+'USDT',Timeframe.DAY)
        gainers[gainer]['trend_h4'] = trend(gainer+'USDT',Timeframe.H4) 
        gainers[gainer]['trend_h1'] = trend(gainer+'USDT',Timeframe.H1) 
    for gainer in gainers.keys():
        thread = Thread(target=_thread_way,kwargs={'gainers':gainers,'gainer':gainer})
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def run():

    gainers,losers = gainers_losers()
    thread1 = Thread(target=append_gainer,kwargs={'gainers':gainers})
    thread1.start()
    thread2 = Thread(target=append_loser,kwargs={'losers':losers})
    thread2.start()
    thread1.join()
    thread2.join()

    df_gainers = pd.DataFrame.from_dict(gainers)#,orient='index')
    df_gainers = df_gainers.transpose()
    # df_gainers.set_index('crypto',inplace=True)
    df_losers = pd.DataFrame.from_dict(losers)#,orient='index')
    df_losers = df_losers.transpose()
    df_gainers.to_json('files/new_gainers.json')
    df_losers.to_json('files/new_losers.json')

def save_gainers_losers():
    func.move_json('./files/new_gainers.json','./files/gainers.json')
    os.remove('./files/new_gainers.json') 
    func.move_json('./files/new_losers.json','./files/losers.json')
    os.remove('./files/new_losers.json') 

