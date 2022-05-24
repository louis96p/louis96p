import pandas as pd
from urllib.request import urlopen
import certifi
import json

column = ("Sympol","date", "close")

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey=7d38e9b8fa6ff6a7d4cd58b5749d5e83")

Stocklist = pd.DataFrame(get_jsonparsed_data(url))
#df_nested_list = pd.json_normalize(Stocklist, record_path =['historical'])
#filter by stock (no ETF or Funds)
Stocklist_F=Stocklist.loc[Stocklist['type'] == "stock"]
Stocklist_F1 = Stocklist_F.drop(Stocklist_F[Stocklist_F['price'] < 0.1 ].index)
Stocklist_F1 ['StockType'] = ['Pennystocks' if x <= 5 else 'Stock' for x in Stocklist_F1['price']]

#save to CSV
#pd.read_json(json.dumps
#Stocklist_F1.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\Ticker.csv", index = None)
print(Stocklist_F1 )



