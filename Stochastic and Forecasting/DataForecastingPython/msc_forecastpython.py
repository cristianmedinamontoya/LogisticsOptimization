import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
sns.set(rc={'figure.figsize':(12,6)})
time_series= pd.read_csv('timeseries.csv',parse_dates=True)
time_series.info()
time_series['date']= pd.to_datetime(time_series['date'])

time_series.head()

time_series= time_series.set_index('date')
monthly_series= time_series.total_revenue.resample('M').sum()

monthly_series.plot()
monthly_series.head()

from pylab import rcParams
rcParams['figure.figsize']=16,8


components= sm.tsa.seasonal_decompose(monthly_series)

###### MA model

model_ma= sm.tsa.statespace.SARIMAX(monthly_series,order= (0,0,1))
results_ma= model_ma.fit()
results_ma.aic

model_AR= sm.tsa.statespace.SARIMAX(monthly_series,order= (1,0,0))
results_AR= model_AR.fit()

results_AR.aic

model_ARma= sm.tsa.statespace.SARIMAX(monthly_series,order= (1,0,1))
results_ARma= model_ARma.fit()

results_ARma.aic

model_ARima= sm.tsa.statespace.SARIMAX(monthly_series,order= (1,1,1))
results_ARima= model_ARima.fit()
results_ARima.aic

results_ARima.plot_diagnostics(figsize=(15, 12))

###### getting the best orders
import itertools       
           
P=D=Q=p=d=q= range(0,3)
S= 12
combinations= list(itertools.product(p,d,q,P,D,Q))
len(combinations)

                              
                              
                              
combinations

arima_orders=[(x[0],x[1],x[2]) for x in combinations]
seasonal_orders=[(x[3],x[4],x[5],S) for x in combinations]

results_data= pd.DataFrame(columns=['p','d','q','P','D','Q','AIC'])

### length of combinatioons

len(combinations) 

for i in range(len(combinations)):
     try:
      
          model = sm.tsa.statespace.SARIMAX(monthly_series,order=arima_orders[i],
                                        seasonal_order= seasonal_orders[i]
                                       )
          result= model.fit()
          results_data.loc[i,'p']= arima_orders[i][0]
          results_data.loc[i,'d']= arima_orders[i][1]
          results_data.loc[i,'q']= arima_orders[i][2]
          results_data.loc[i,'P']= seasonal_orders[i][0]
          results_data.loc[i,'D']= seasonal_orders[i][1]
          results_data.loc[i,'Q']= seasonal_orders[i][2]
          results_data.loc[i,'AIC']= result.aic
     except:
          continue
      