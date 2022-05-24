from operator import index
import numpy as np
from numpy import arange
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import LassoCV
import pickle
from sklearn.model_selection import RepeatedKFold
from sklearn import metrics
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import max_error
from sklearn.metrics import mean_squared_error


CompanyKPI_read = pd.read_csv ("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\TotalData.csv")
CompanyKPI= pd.DataFrame(CompanyKPI_read)
#CompanyKPIb = CompanyKPI#.replace('Financial', "Financial Services").replace('Textiles, Apparel & Luxury Goods', "Consumer products").replace('Road & Rail', "Logistics & Transportation").replace('Telecommunication', "Technology").replace('Aerospace & Defense', "Airlines").replace('Banking', "Financial Services").replace('Construction', "Building")
#Cprofile_read = pd.read_csv ("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companyprofileTotal.csv")
allsectors = pd.DataFrame(CompanyKPI, columns =['sector'])
Allsectors_u = allsectors.drop_duplicates()
print(Allsectors_u)
List = []
List2 = []
MetricsName = ['Alpha','R2Score','absolut_error','max_error','mean_squared_error']
CoeffName = ["revenuePerShare_x","netIncomePerShare_x","operatingCashFlowPerShare_x","freeCashFlowPerShare_x","bookValuePerShare_x",
"shareholdersEquityPerShare_x","peRatio_x","priceToSalesRatio_x","pbRatio_x","enterpriseValueOverEBITDA_x","debtToEquity_x","debtToAssets_x",
"currentRatio_x","payoutRatio_x","workingCapital_x","investedCapital_x","roe_x","dcf_x","netIncomePerShare_S","operatingCashFlowPerShare_S",
"peRatio_S","pbRatio_S", "enterpriseValueOverEBITDA_S","debtToEquity_S","workingCapital_S","debtToAssets_S","currentRatio_S","payoutRatio_S",
"roe_S","investedCapital_S","price"]



Sector = Allsectors_u['sector'].values.tolist()

#Sector = ['Technology', "Consumer products"]
for i in Sector:
    print(CompanyKPI.loc[CompanyKPI['sector'] == i ])
    CKPI = CompanyKPI.loc[CompanyKPI['sector'] == i ].drop(columns=['symbol','date_new','name','period','sector','StockType'])
    CKPI.dropna(inplace = True)
    #print (Cad.isna().sum()) 
    X = CKPI.drop('FuturePrice', axis=1)
    Y = CKPI['FuturePrice']
    

    train_X, test_X, train_y, test_y = train_test_split(X,Y, random_state=1)

    #https://machinelearningmastery.com/lasso-regression-with-python/
    cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)
    model = LassoCV(alphas=arange(0, 10, 0.01), cv=cv, n_jobs=-1)
    model.fit(train_X, train_y)
    # summarize chosen configuration
    print('alpha: %f' % model.alpha_)

   
    lasso_reg = linear_model.Lasso(random_state=1, alpha = model.alpha_)
    lasso_reg.fit(train_X, train_y)
   

    coef = pd.DataFrame(np.transpose(lasso_reg.coef_),  columns = [i])
    List2.append(coef)
    
    y_true = test_y.values.tolist()
    y_pred =lasso_reg.predict(test_X)
    


    Metrics = [ model.alpha_, metrics.r2_score(y_true,y_pred), metrics.mean_absolute_error(y_true,y_pred),metrics.max_error(y_true,y_pred),metrics.mean_squared_error(y_true,y_pred)]
    
    df = pd.DataFrame (Metrics, columns = [i])
    List.append(df)
    print (df)


    filename = ("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\Models\\model_" + i + ".pkl")
    All = pickle.dump(lasso_reg, open(filename, 'wb'))
    
    
Cooncat = pd.concat(List, axis=1, join="inner")
Cooncat2 = pd.concat(List2, axis=1, join="inner")

Cooncat['Metrics'] = MetricsName
first_column = Cooncat.pop('Metrics')
Cooncat.insert(0, 'Metrics', first_column)
#oncat = test.merge(Cooncat)
print (Cooncat)
Cooncat.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\ModelMetrics.csv", index = None)
Cooncat2['KPis'] = CoeffName
first_column = Cooncat2.pop('KPis')
Cooncat2.insert(0, 'KPis', first_column)
Cooncat2.to_csv (r"C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\ModelCoef.csv", index = None)
print (Cooncat2)
