# -*- coding: utf-8 -*-
"""optimize portfolio

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Iz5XkUBVOr36ZrS_EwQW4hmeF0wW-cVs
"""

# Description: This program attempts to optimize a users portfolio using the Efficient Frontier & Python.

# Import the python libraries
from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#FAANG
assets =  [ 'VTV','VOE', 'VBR' ,'IWD', 'IWN','IWS','IJS', 'EFV']

# Assign weights to the stocks. Weights must = 1 

weights = []
for num in assets:
  weights.append(1/len(assets))
weights = np.array(weights)
#weights = np.array([0.053966,0.128607, 0.057119, 0.170256, 0.26572, 0.186708, 0.137591,0,0,0,0,0,0,0,0,0,0 ])

weights

#Get the stock starting date
stockStartDate = '2000-01-01'
# Get the stocks ending date aka todays date and format it in the form YYYY-MM-DD
today = datetime.today().strftime('%Y-%m-%d')

#Create a dataframe to store the adjusted close price of the stocks
df = pd.DataFrame()
#Store the adjusted close price of stock into the data frame
for stock in assets:
   df[stock] = web.DataReader(stock,data_source='yahoo',start=stockStartDate , end=today)['Adj Close']

df

# Create the title 'Portfolio Adj Close Price History
title = 'Portfolio Adj. Close Price History'

#Get the stocks
my_stocks = df

#Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5

# Loop through each stock and plot the Adj Close for each day
for c in my_stocks.columns.values:
  plt.plot( my_stocks[c],  label=c)

#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.title(title)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Adj. Price USD ($)',fontsize=18)
plt.legend(my_stocks.columns.values, loc='upper left')
plt.show()

#Show the daily simple returns, NOTE: Formula = new_price/old_price - 1
returns = df.pct_change()
returns

#covariance matrix
cov_matrix_annual = returns.cov() * 252
cov_matrix_annual

#calculate the portfolio variance
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
port_variance

#calculate the portfolio volatility aka std
port_volatility = np.sqrt(port_variance)
port_volatility

#calculate the annual portfolio return
portfolioSimpleAnnualReturn = np.sum(returns.mean()*weights) * 252
portfolioSimpleAnnualReturn

#show expected annual return, volatility and variance
percent_var = str(round(port_variance, 2) * 100) + '%'
percent_vols = str(round(port_volatility, 2) * 100) + '%'
percent_ret = str(round(portfolioSimpleAnnualReturn, 2)*100)+'%'

print("Expected annual return : "+ percent_ret)
print('Annual volatility/standard deviation/risk : '+percent_vols)
print('Annual variance : '+percent_var)

#pip install PyPortfolioOpt

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

#portfolio optimization

#calculate the expected returns and the annualised sample covariance matrix of asset returns
mu = expected_returns.mean_historical_return(df) #returns.mean() * 252
S = risk_models.sample_cov(df) #Get the sample covariance matrix

#maximize for max sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe() #Maximize the Sharpe ratio, and get the raw weights
cleaned_weights = ef.clean_weights() 
print(cleaned_weights) #Note the weights may have some rounding error, meaning they may not add up exactly to 1 but should be close
ef.portfolio_performance(verbose=True)

#get the discrete number of shares
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
latest_prices = get_latest_prices(df)
weights = cleaned_weights 
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = 1200)
allocation, leftover = da.lp_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))

