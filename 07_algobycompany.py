import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import LassoCV
import pickle

CompanyKPI_read = pd.read_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\merge_v1.csv")
Cprofile_read = pd.read_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\CProfile\\companyprofileTotal.csv")
CompanyKPI= pd.DataFrame(CompanyKPI_read)
CompanyProfil= pd.DataFrame(Cprofile_read,columns =["symbol","sector"])
print(CompanyProfil)

Company = "CMCSA"

TestData = CompanyKPI.loc[CompanyKPI['symbol'] == Company ].drop(columns=['symbol','date_new','period','sector','StockType'])

Sector = CompanyProfil.loc[CompanyProfil['symbol'] == Company ].drop(columns=['symbol'])
Sector2 = Sector.iloc[0]['sector']

XC = TestData.drop('FuturePrice', axis=1)
YC = TestData['FuturePrice']
#train_XC, test_XC, train_yc, test_yc = train_test_split(XC,YC)


filename = open("C://Users//DELPILL2//OneDrive - EY//Documents//Privat//Python//Sample//Models//model_" + Sector2 + ".pkl",'rb')
loaded_model = pickle.load(filename)

result = pd.DataFrame(loaded_model.predict(XC))
print (TestData)
print (result)


