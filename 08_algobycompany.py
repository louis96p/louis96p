from os import rename
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import LassoCV
import pickle

CompanyKPI_read = pd.read_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\TotalData.csv")
CompanyKPI= pd.DataFrame(CompanyKPI_read)
CompanyProfil= pd.DataFrame(CompanyKPI_read,columns =["symbol","sector"])
CompanyProfil_d = CompanyProfil.drop_duplicates()

#CompanyProfil_d.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\PredictData - Kopie.csv", index = None)

List= []
#Company = ['WFC']
Company= CompanyProfil_d['symbol'].values.tolist()
for i in Company:
    CompanyData = CompanyKPI.loc[CompanyKPI['symbol'] == i ]
    CompanyData.reset_index(inplace = True, drop = True)
    TestData = CompanyKPI.loc[CompanyKPI['symbol'] == i ].drop(columns=['symbol','date_new','period','sector','StockType'])
    print (TestData)
    Sector = CompanyProfil.loc[CompanyProfil['symbol'] == i ].drop(columns=['symbol'])
    Sector2 = Sector.iloc[0]['sector']

    XC = TestData.drop('FuturePrice', axis=1)
    YC = TestData['FuturePrice']
    print(XC)
    #train_XC, test_XC, train_yc, test_yc = train_test_split(XC,YC)
    XC.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\PredictData - Kopie.csv", index = None)

    filename = open("C://Users//DELPILL2//OneDrive - EY//Documents//Privat//Python//Sample//Models//model_" + Sector2 + ".pkl",'rb')
    loaded_model = pickle.load(filename)
    print(filename)
    result = pd.DataFrame(loaded_model.predict(XC))
    print (result)
    result.rename(columns={0:"FuturePrice_Prediction"},inplace=True)
    CompanyPre = CompanyData.join(result)
    print(CompanyPre)
    CompanyPre['CAGR'] = ((CompanyPre ['FuturePrice_Prediction'] / CompanyPre ['price'])**(1/5.0)-1)*100
    #CompanyPre['recommendation'] = 
    CompanyPre.loc[CompanyPre['CAGR'] < 7 , 'recommendation'] = "hold" 
    CompanyPre.loc[CompanyPre['CAGR'] > 7 , 'recommendation'] = "buy" 
    CompanyPre.loc[CompanyPre['CAGR'] < 2 , 'recommendation'] = "sell"
    CompanyPre.loc[CompanyPre['CAGR'] < -1 , 'recommendation'] = "short"

    Prediction = pd.DataFrame(CompanyPre,columns =["symbol","date_new","price","FuturePrice_Prediction","CAGR","recommendation"]).head(1)
    List.append(Prediction)
Predict = pd.concat(List)

Predict.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\PredictData.csv", index = None)

print(Predict)