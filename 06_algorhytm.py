from typing import List
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

CompanyKPI_read = pd.read_csv ("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\TotalData.csv")
CompanyKPI= pd.DataFrame(CompanyKPI_read)
CompanyKPIb = CompanyKPI.replace('Financial', "Financial Services").replace('Textiles, Apparel & Luxury Goods', "Consumer products").replace('Road & Rail', "Logistics & Transportation").replace('Telecommunication', "Technology").replace('Aerospace & Defense', "Airlines").replace('Banking', "Financial Services")
#Cprofile_read = pd.read_csv ("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\StockKpi\\companyprofileTotal.csv")
allsectors = pd.DataFrame(CompanyKPIb, columns =['sector'])
Allsectors_u = allsectors.drop_duplicates()
print(Allsectors_u)
List = []
Sector = Allsectors_u['sector'].values.tolist()

#Sector = ['Aerospace & Defense','Trading Companies & Distributors','Commercial Services & Supplies']
for i in Sector:
    print(CompanyKPIb.loc[CompanyKPIb['sector'] == i ])
    CKPI = CompanyKPIb.loc[CompanyKPIb['sector'] == i ].drop(columns=['symbol','date_new','period','sector','StockType'])
    CKPI.dropna(inplace = True)
    #print (Cad.isna().sum()) 
    X = CKPI.drop('FuturePrice', axis=1)
    Y = CKPI['FuturePrice']
    #https://machinelearningmastery.com/lasso-regression-with-python/

    train_X, test_X, train_y, test_y = train_test_split(X,Y, random_state=1)

    cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)
    model = LassoCV(alphas=arange(0, 1, 0.01), cv=cv, n_jobs=-1)
    model.fit(train_X, train_y)
    # summarize chosen configuration
    print('alpha: %f' % model.alpha_)



    lasso_reg = linear_model.Lasso(alpha=model.alpha_)
    lasso_reg.fit(train_X, train_y)
   
    print (lasso_reg.score(train_X, train_y))
    print (lasso_reg.score(test_X, test_y))
    
    Coef = pd.DataFrame(lasso_reg.coef_, index = train_X.columns )
    print (Coef)
    filename = ("C:\\Users\\DELPILL2\\OneDrive - EY\\Documents\\Privat\\Python\\Sample\\Models\\model_" + i + ".pkl")
    All = pickle.dump(lasso_reg, open(filename, 'wb'))
    
   # App = Coef.append(Coef)


    #loaded_model = pickle.load(open(filename, 'rb'))
    
    #result = loaded_model.score(test_X, test_y)
    #print(result)
    
#Cooncat = pd.concat(App)
#print (Cooncat)