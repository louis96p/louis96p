
import numpy as np
import pandas as pd
from urllib.request import urlopen
import certifi
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as snCprofile_Ticker_merge


Company_kpi_read = pd.read_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companystock_kpi.csv")
Company_kpi= pd.DataFrame(Company_kpi_read) 
Company_kpi['date']= Company_kpi['date'].str[:10]


Company_price_dcf_read = pd.read_csv(r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companystock_dfc.csv")
Company_price_dcf= pd.DataFrame(Company_price_dcf_read).sort_values(by='date', ascending=True)
Company_price_dcf['date']= Company_price_dcf['date'].str[:10]



Company_Profile_read = pd.read_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companyprofileTotal_1.csv")
Company_Profile= pd.DataFrame(Company_Profile_read, columns =["symbol","StockType","sector","name"])
Stock_merge = Company_kpi.merge(Company_price_dcf, how='left', left_on=['date', 'symbol'], right_on=['date', 'symbol'])

Stock_merge ['Year']= Stock_merge ['date'].str[:4]
Stock_merge.loc[Stock_merge ['period'] == 'Q1' , 'date'] = '31-03' 
Stock_merge.loc[Stock_merge ['period'] == 'Q2' , 'date'] = '30-06' 
Stock_merge.loc[Stock_merge ['period'] == 'Q3' , 'date'] = '30-09' 
Stock_merge.loc[Stock_merge ['period'] == 'Q4' , 'date'] = '31-12' 
Stock_merge ['date_new'] = Stock_merge ['date'] + "-" + Stock_merge ['Year']
Stock_merge ['date_new']= pd.to_datetime(Stock_merge['date_new'], utc = False)
print (Stock_merge)

##Set Price 5 years back 
FuturePrice= pd.DataFrame(Stock_merge, columns = ['symbol','price', 'date','Year'])
FuturePrice['Year'] = FuturePrice['Year'].astype(int)
FuturePrice['Year'] = FuturePrice['Year'] - 5
FuturePrice['Year'] = FuturePrice['Year'].astype(str)
FuturePrice['FutureDate'] = FuturePrice['date'] + "-" + FuturePrice['Year']
FuturePrice['FutureDate']= pd.to_datetime(FuturePrice['FutureDate'], utc = False)
FuturePrice.rename(columns = {'price':'FuturePrice'}, inplace = True)
FuturePrice.pop("date")
FuturePrice.pop("Year")

print (FuturePrice)
Stock_merge_future = Stock_merge.merge(FuturePrice, how='left', left_on=['date_new', 'symbol'], right_on=['FutureDate', 'symbol'])
Stock_merge_future.pop("date")
Stock_merge_future.pop("FutureDate")


StockTotal = pd.merge(Stock_merge_future, Company_Profile, on="symbol")
StockTotal_R = StockTotal.replace('Financial', "Financial Services").replace('Textiles, Apparel & Luxury Goods', "Consumer products").replace('Road & Rail',
 "Logistics & Transportation").replace('Aerospace & Defense', "Airlines").replace('Banking', "Financial Services").replace('Construction', 
"Building").replace('Professional Services', "Services").replace('Telecommunication', "Technology")
#Filter by sector
Sector = StockTotal_R.groupby(['sector','date_new']).mean()
Sector.pop("price")
Sector.pop("FuturePrice")
print(Sector.dtypes) 
Stock_sector = StockTotal_R.merge(Sector, how='left', left_on=['date_new', 'sector'], right_on=['date_new', 'sector'])
print(Stock_sector) 



Stock_sector['netIncomePerShare_S'] = Stock_sector ['netIncomePerShare_y'] - Stock_sector ['netIncomePerShare_x']
Stock_sector['operatingCashFlowPerShare_S'] = Stock_sector ['operatingCashFlowPerShare_x'] -  Stock_sector ['operatingCashFlowPerShare_x']
Stock_sector ['peRatio_S'] = Stock_sector ['peRatio_y'] -  Stock_sector ['peRatio_x']
Stock_sector ['pbRatio_S'] = Stock_sector ['pbRatio_y'] -  Stock_sector ['pbRatio_x']
Stock_sector ['enterpriseValueOverEBITDA_S'] = Stock_sector ['enterpriseValueOverEBITDA_y'] -  Stock_sector ['enterpriseValueOverEBITDA_x']
Stock_sector ['debtToEquity_S'] = Stock_sector ['debtToEquity_y'] -  Stock_sector ['debtToEquity_x']
Stock_sector ['workingCapital_S'] = Stock_sector ['workingCapital_y'] -  Stock_sector ['workingCapital_x']
Stock_sector ['debtToAssets_S'] = Stock_sector ['debtToAssets_y'] -  Stock_sector ['debtToAssets_x']
Stock_sector ['currentRatio_S'] = Stock_sector ['currentRatio_y'] -  Stock_sector ['currentRatio_x']
Stock_sector ['payoutRatio_S'] = Stock_sector ['payoutRatio_y'] -  Stock_sector ['payoutRatio_x']
Stock_sector ['roe_S'] = Stock_sector ['roe_y'] -  Stock_sector ['roe_x']
Stock_sector ['investedCapital_S'] = Stock_sector ['investedCapital_y'] -  Stock_sector ['investedCapital_x']

print (Stock_sector.dtypes)
StockTotal_filtered = pd.DataFrame(Stock_sector , columns=["symbol","name","date_new","period","StockType","sector","revenuePerShare_x","netIncomePerShare_x","operatingCashFlowPerShare_x","freeCashFlowPerShare_x","bookValuePerShare_x",
"shareholdersEquityPerShare_x","peRatio_x","priceToSalesRatio_x","pbRatio_x","enterpriseValueOverEBITDA_x","debtToEquity_x","debtToAssets_x",
"currentRatio_x","payoutRatio_x","workingCapital_x","investedCapital_x","roe_x","dcf_x","netIncomePerShare_S",
"operatingCashFlowPerShare_S","peRatio_S","pbRatio_S",
"enterpriseValueOverEBITDA_S","debtToEquity_S","workingCapital_S","debtToAssets_S","currentRatio_S","payoutRatio_S",
"roe_S","investedCapital_S","price","FuturePrice"])



#StockTotal_filtered.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documen\\Privat\\Python\\Sample\\StockKpi\\TotalData.csv", index = None)
res = StockTotal_filtered[~(StockTotal_filtered['date_new'] < '2010-01-01')]
res.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\TotalData.csv", index = None)

print(res)


