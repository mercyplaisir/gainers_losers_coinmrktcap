import json

import pandas as pd

def save_soup(data,filepath):
    with open(filepath,'w') as f:
        f.write(data)
    return

def load_data_json(filepath):
    with open(filepath,'r') as f:
        data = json.load(f)

    data = pd.DataFrame.from_dict(data)
    return data
def dump_data_json(filepath,data):
    
    with open(filepath,'w') as f:
        f.write(data)

def list_comparison(old:list,new:list):
    new_items = []
    for item in new:
        if item not in old:
            new_items.append(item)
    return new_items

index = lambda a : list(a.index)

def move_json(oldfile,newfile):
    d = load_data_json(oldfile).to_json()
    
    dump_data_json(newfile,d)