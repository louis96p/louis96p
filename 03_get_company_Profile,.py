import numpy as np
import pandas as pd
from urllib.request import urlopen
import certifi
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sn
import time

#Access to the API
APIKEY = "?apikey=7d38e9b8fa6ff6a7d4cd58b5749d5e83"

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)



Stocklist_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\Ticker.csv")
Stocklist = pd.DataFrame(Stocklist_read, columns =["symbol", "StockType"])
Stocklist_F=Stocklist.loc[Stocklist['StockType'] == "Stock"].head(29000)
#Loop to get multiple company data
#List = ["AAPL", "MSFT", "INTC", "TSLA"]
ListTotal= Stocklist_F['symbol'].values.tolist()
max_batch = 750
CompanyInfoListTotal = []
for i in range(21500, len(ListTotal), max_batch):
    List = (ListTotal[i:i+max_batch]) #the_list_reference[start:end:steps]
    
    L_CompanyInfoList = [] 
    for Code in List:
     url =  ("https://financialmodelingprep.com/api/v3/profile/" + Code + APIKEY)
     L_CompanyInfo = pd.read_json(url)
     #Stocks = pd.json_normalize(Stocklist,  meta=['symbol'],record_path =['historical'])
     L_CompanyInfoList.append(L_CompanyInfo) #save all dataframes from loop in a list
    CompanyInforConcat= pd.concat(L_CompanyInfoList) #merge all dataframes to one 
    #F_CompanyInfo =pd.DataFrame(CompanyInforConcat, columns =["symbol","mktCap","industry", "sector", "country","isActivelyTrading", "lastDiv","beta"])
    #CompanyInforConcat.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_300.csv", index = None)
    #print (F_CompanyInfo)
    time.sleep(60)
    CompanyInfoListTotal.append(CompanyInforConcat) #save all dataframes from loop in a list
CompanyInforConcatTotal= pd.concat(CompanyInfoListTotal) #merge all dataframes to one 
F_CompanyInfo =pd.DataFrame(CompanyInforConcatTotal, columns =["symbol","mktCap","industry", "sector", "country","isActivelyTrading", "lastDiv","beta"])
F_CompanyInfo.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_7500_4.csv", index = None)
print (F_CompanyInfo)

#CompanyInforConcatTotal= pd.concat(L_CompanyInfoList)
#print (CompanyInforConcatTotal)
#F_CompanyInfo.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_300.csv", index = None)
#print(F_CompanyInfo)
#print(CompanyInforConcat.dtypes)
#print(ListB)
