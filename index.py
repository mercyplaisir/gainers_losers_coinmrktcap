import pandas as pd
import json

import func
import coinmktcap

# get gainers and losers
coinmktcap.run()

# old
old_gainers = func.index(func.load_data_json('./files/gainers.json'))
old_losers = func.index(func.load_data_json('./files/losers.json'))

# new
new_gainers = func.index(func.load_data_json('./files/new_gainers.json'))
new_losers =func.index( func.load_data_json('./files/new_losers.json'))

new_gainers_items = func.list_comparison(old_gainers,new_gainers)
new_losers_items = func.list_comparison(old_losers,new_losers)

# close by saving new data
# coinmktcap.save_gainers_losers()