from pickle import LIST
import numpy as np
import pandas as pd
from urllib.request import urlopen
import certifi
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sn


CompanyProfil_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companyprofile_1.csv")
CompanyProfil= pd.DataFrame(CompanyProfil_read) 

Ticker_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\Ticker.csv")
Ticker= pd.DataFrame(Ticker_read) 

Cprofile_Ticker_merge = pd.merge(CompanyProfil, Ticker, on="symbol")#.set_index("symbol")
Cprofile_Ticker_merge.pop("type")
Cprofile_Ticker_merge_F = Cprofile_Ticker_merge[Cprofile_Ticker_merge['isActivelyTrading'] == True]
Cprofile = Cprofile_Ticker_merge_F[Cprofile_Ticker_merge_F['sector'].notna()]
Cprofile.loc[Cprofile['lastDiv'] >0.01 , 'StockType'] = "ValueStock" 
Cprofile.loc[Cprofile['lastDiv'] < 0  , 'StockType'] = "GrowStock"
Cprofile.loc[Cprofile['mktCap'] > 1000000000 , 'StockType'] = "ValueStock"
Cprofile.loc[Cprofile['price'] < 1.01 , 'StockType'] = "PennyStock"
Cprofile1= Cprofile.drop(Cprofile[Cprofile['price'] < 1.01 ].index)

Cprofile_F = pd.DataFrame(Cprofile1, columns =["symbol", "name", "sector", "country", "exchangeShortName","mktCap","beta","StockType"])
print(Cprofile_F)
Cprofile_F.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companyprofileTotal_1.csv", index = None)
#print (W_CompanyInfo.loc[W_CompanyInfo['StockType'] == "GrowStock"])
