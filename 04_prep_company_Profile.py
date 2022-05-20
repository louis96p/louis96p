from pickle import LIST
import numpy as np
import pandas as pd
from urllib.request import urlopen
import certifi
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sn


CompanyProfil_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_7500.csv")
CompanyProfil= pd.DataFrame(CompanyProfil_read) 

CompanyProfil1_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_7500_2.csv")
CompanyProfil1= pd.DataFrame(CompanyProfil1_read) 

CompanyProfil2_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_7500_3.csv")
CompanyProfil2= pd.DataFrame(CompanyProfil2_read) 

CompanyProfil3_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_7500_4.csv")
CompanyProfil3= pd.DataFrame(CompanyProfil3_read) 

CompanyProfilP_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofile_penny.csv")
CompanyProfilP= pd.DataFrame(CompanyProfilP_read) 

Ticker_read = pd.read_csv("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\Ticker.csv")
Ticker= pd.DataFrame(Ticker_read) 


Dataframes = [CompanyProfil, CompanyProfil1, CompanyProfil2,CompanyProfil3, CompanyProfilP]

CompanyProfil_C = pd.concat(Dataframes)
CompanyProfil = pd.DataFrame(CompanyProfil_C)
#print (CompanyProfil_C)

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
Cprofile_F.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofileTotal.csv", index = None)
#print (W_CompanyInfo.loc[W_CompanyInfo['StockType'] == "GrowStock"])
