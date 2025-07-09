import os

SENDORDER:bool = False # to send orders on the exchange
TELEGRAM_UPDATE:bool = True # to send message on telegram
MESSAGEID:int = 0

GN_LOS_MESSAGE_ID = 1303
ACC_INFO_ID = 1304

NOTIONAL = 10
LEVERAGE = 5

API_TOKEN = os.getenv('TELEGRAM')
CHATID = os.getenv('CHATID')
CHANNELID= os.getenv('CHANNELID')
