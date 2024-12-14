from submodules.binance_handler.futures import binance_handler
from submodules.binance_handler.errors import errors
from submodules.binance_handler.futures import order , leverage
import func


def send_buy_order(item:str):
    try:
        _order = order.market_buy_order(symbol=item+"USDT", quantity= binance_handler.minimum_quantity(item+"USDT"))
        func._save_order(_order)
        
    except errors.SymbolNotFound:
        print(f"{__name__} - {item} was not found")
    except errors.OrderNotSent:
        print(f"{__name__} - order for {item}  not sent")
        pass
    except errors.QuantityLessOrEqualToZero:
        print(f"{item} -quantity less or equal to zero \n we pass it")
        pass

def send_sell_order(item:str):
    try:
        _order = order.market_sell_order(item+"USDT", binance_handler.minimum_quantity(item+"USDT")) #.minimum_quantity(item+"USDT"))
    # telegram.send_message(bot=bot,message=f"sold {item}")
        func._save_order(_order)
    except errors.SymbolNotFound:
        print(f"{__name__} - - {item} was not found")
        pass
    except errors.OrderNotSent:
        print(f"{__name__} -  - order for {item}  not sent")
        pass
    except errors.QuantityLessOrEqualToZero:
        print(f"{item} -quantity less or equal to zero \n we pass it")
        pass


def _quantity_notional(symbol,notional:int|float):
    symbol_price = binance_handler.pair_price(symbol)
    
    return binance_handler._quantity_precision(amount=notional/symbol_price,symbol=symbol)



def send_buy_order_notional(item:str,notional:int|float,leverage_amount:int):
    try:
        _quantity = _quantity_notional(item+"USDT",notional)
        leverage.leverage(symbol=item+"USDT",leverage=leverage_amount)
        _order = order.market_buy_order(symbol=item+"USDT",quantity=_quantity)# quantity= binance_handler.minimum_quantity(item+"USDT"))
        func._save_order(_order)
        
    except errors.SymbolNotFound:
        print(f"{__name__} - {item} was not found")
    except errors.OrderNotSent:
        print(f"{__name__} - order for {item}  not sent")
        pass
    except errors.QuantityLessOrEqualToZero:
        print(f"{item} -quantity less or equal to zero \n we pass it")
        pass

def send_sell_order_notional(item:str,notional:int|float,leverage_amount:int):
    try:
        _quantity = _quantity_notional(item+"USDT",notional)
        leverage.leverage(symbol=item+"USDT",leverage=leverage_amount)
        _order = order.market_sell_order(item+"USDT",quantity=_quantity)# binance_handler.minimum_quantity(item+"USDT")) #.minimum_quantity(item+"USDT"))
    # telegram.send_message(bot=bot,message=f"sold {item}")
        func._save_order(_order)
    except errors.SymbolNotFound:
        print(f"{__name__} - - {item} was not found")
        pass
    except errors.OrderNotSent:
        print(f"{__name__} -  - order for {item}  not sent")
        pass
    except errors.QuantityLessOrEqualToZero:
        print(f"{item} -quantity less or equal to zero \n we pass it")
        pass