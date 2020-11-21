#Option Pricing
#Evaluating investment opportunities based on the comparison of the intrinsic vs. actually traded values of European options

#___________________________________________________________________________________

#1. Preparation

#Install yfinance in case of issues see https://github.com/ranaroussi/yfinance

pip install yfinance

#Import libraries and modules

import yfinance as yf
import numpy as np
import pandas as pd
import datetime
import math
from dateutil.relativedelta import relativedelta

#___________________________________________________________________________________

#2. Ask for user inputs

#Ask for ticker
while True:
    ticker = yf.Ticker(input("Please enter ticker for option you want to calculate (e.g. AAPL, AMZN...): "))
    if not ticker.options:
        print("Please enter a correct ticker. You can find them on finance.yahoo.com")
        continue
    else:
        break
#Ask for expiration date
while True:    
    try:
        print("Choose an expiration date and enter it below", ticker.options)
        expiration = input("Enter expiration date (yyyy-mm-dd): ")
        opt = ticker.option_chain(expiration)
    except ValueError:
        print("Please choose a date from the list above. Keep the formatting!")
        continue
    else:
        break
#Ask for type of option and create dataframe with options of that type
while True:
    try:
        opttype = input("Enter option type (puts/calls): ")
        df = getattr(opt,opttype)
    except AttributeError:
        print("Please enter only puts or calls !")
        continue
    else:
        break
#Ask for strike of option and selecting option closest to user input
while True:
    try:
        option_chosen = df.iloc[(df['strike']-float(input("Please enter strike: "))).abs().argsort()[:1]]
    except ValueError:
        print("Please enter a numeric value.")
        continue
    else:
        break
#___________________________________________________________________________________

#3. Get additional data from yahoo finance

#Get closest strike, current price and volatility of the chosen option and tell the user what the actual strike is          
strike = option_chosen.iloc[0]["strike"]
price = option_chosen.iloc[0]["ask"]
volatility = option_chosen.iloc[0]["impliedVolatility"]
print("The closest currently traded strike is: ", strike)


#Timedelta for function, time to maturity in years
today = datetime.datetime.today()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
expiration_datetime = datetime.datetime.strptime(expiration, '%Y-%m-%d')
delta= expiration_datetime - today
time_to_maturity=delta.days/365
    
#Stockprice    
hist = ticker.history(period="max")
hist = hist.tail(1)
stockprice = hist.iloc[0]["Open"]

#Risk free rate
risk_free = yf.Ticker("^IRX")
hist = risk_free.history()
hist = hist.tail(1)
r = hist.iloc[0]["Open"]/100

#Dividend approximation based on historic dividend returns. 
dividend = hist["Dividends"]
delta_years_floor = math.floor(time_to_maturity)
delta_years_ceil = delta_years_floor + 1
prior_year_t = today - relativedelta(years=1)
prior_year_expiration = expiration_datetime - relativedelta(years=delta_years_ceil)
dividend_approx = sum(dividend.loc[prior_year_t:today])*delta_years_floor
dividend_approx = dividend_approx + sum(dividend.loc[prior_year_t:prior_year_expiration])

#___________________________________________________________________________________

#4. Definition of four functions for different option types

def European_Call_Div (S0, K, T, sigma, n):

#Calculation of Initial Parameters
  dt = T/n
  u = np.exp(sigma*np.sqrt(dt))
  d = 1/u
  DivRate = dividend_approx / S0
  ContAnDivRate = np.log(1+DivRate)
  p = (np.exp((r-ContAnDivRate)*dt)-d)/(u-d)

#Price tree
  # Store the price tree in a square matirx 
  price_tree = np.zeros([n+1, n+1])

  #Calculate the stock price on each note
  for i in range (n+1):
    for j in range (i+1):
      price_tree[j,i] = S0*(d**j)*(u**(i-j))

  #Calculate the option value at each node
  option = np.zeros([n+1, n+1])
  
  #Determine the value of the call option at maturity
  option[:, n] = np.maximum(np.zeros(n+1), price_tree[:, n]-K)

  #Iterate backwards the value of the call option
  for i in np.arange(n-1, -1, -1):
    for j in np.arange(0,i+1):
      option[j, i] = np.exp(-r*dt)*(p*option[j, i+1]+(1-p)*option[j+1, i+1])

  #Return
  return option[0, 0]

def European_Call (S0, K, T, sigma, n):
#Calculation of Initial Parameters
  dt = T/n
  u = np.exp(sigma*np.sqrt(dt))
  d = 1/u
  p = (np.exp(r*dt)-d)/(u-d)

#Price tree
  # Store the price tree in a square matirx 
  price_tree = np.zeros([n+1, n+1])

  #Calculate the stock price on each note
  for i in range (n+1):
    for j in range (i+1):
      price_tree[j,i] = S0*(d**j)*(u**(i-j))

  #Calculate the option value at each node
  option = np.zeros([n+1, n+1])
  
  #Determine the value of the call option at maturity
  option[:, n] = np.maximum(np.zeros(n+1), price_tree[:, n]-K)

  #Iterate backwards the value of the call option
  for i in np.arange(n-1, -1, -1):
    for j in np.arange(0,i+1):
      option[j, i] = np.exp(-r*dt)*(p*option[j, i+1]+(1-p)*option[j+1, i+1])

  #Return
  return option[0, 0]

def European_Put_Div (S0, K, T, sigma, n):

#Calculation of Initial Parameters
  dt = T/n
  u = np.exp(sigma*np.sqrt(dt))
  d = 1/u
  DivRate = dividend_approx / S0
  ContAnDivRate = np.log(1+DivRate)
  p = (np.exp((r-ContAnDivRate)*dt)-d)/(u-d)

#Price tree
 # Store the price tree in a square matirx 
  price_tree = np.zeros([n+1, n+1])

  #Calculate the stock price on each note
  for i in range (n+1):
    for j in range (i+1):
      price_tree[j,i] = S0*(d**j)*(u**(i-j))

 #Calculate the option value at each node
  option = np.zeros([n+1, n+1])
  
 #Determine the value of the put option at maturity
  option[:, n] = np.maximum(np.zeros(n+1), K-price_tree[:, n])

 #Iterate backwards the value of the put option
  for i in np.arange(n-1, -1, -1):
    for j in np.arange(0,i+1):
      option[j, i] = np.exp(-r*dt)*(p*option[j, i+1]+(1-p)*option[j+1, i+1])

 #Return
  return option[0, 0]

def European_Put (S0, K, T, sigma, n):

#Calculation of Initial Parameters
  dt = T/n
  u = np.exp(sigma*np.sqrt(dt))
  d = 1/u
  p = (np.exp(r*dt)-d)/(u-d)

#Price tree
  # Store the price tree in a square matirx 
  price_tree = np.zeros([n+1, n+1])

  #Calculate the stock price on each note
  for i in range (n+1):
    for j in range (i+1):
      price_tree[j,i] = S0*(d**j)*(u**(i-j))

  #Calculate the option value at each node
  option = np.zeros([n+1, n+1])
  
  #Determine the value of the call option at maturity
  option[:, n] = np.maximum(np.zeros(n+1), K-price_tree[:, n])

  #Iterate backwards the value of the call option
  for i in np.arange(n-1, -1, -1):
    for j in np.arange(0,i+1):
      option[j, i] = np.exp(-r*dt)*(p*option[j, i+1]+(1-p)*option[j+1, i+1])

  #Return
  return option[0, 0]

#___________________________________________________________________________________

#5. Final calculation
#Choosing the correct funtion for the bond and comparing the currently traded price to the intrinsic output price of our funtion
if opttype == "calls" and dividend_approx == 0:
    pred_price=European_Call(stockprice, strike, time_to_maturity,volatility,50)
    print("The intrinsic value of the option is: ",pred_price)
    print("The currently traded price is:",price)
elif opttype == "calls" and dividend_approx > 0:
    pred_price=European_Call_Div(stockprice, strike, time_to_maturity,volatility,50)
    print("The intrinsic value of the option is: ",pred_price)
    print("The currently traded price is:",price)
elif opttype == "puts" and dividend_approx == 0:
    pred_price=European_Put(stockprice, strike, time_to_maturity,volatility,50)
    print("The intrinsic value of the option is: ",pred_price)
    print("The currently traded price is:",price)
else:
    pred_price=European_Put_Div(stockprice, strike, time_to_maturity,volatility,50)
    print("The intrinsic value of the option is: ",pred_price)
    print("The currently traded price is:",price)
    
#Give a recommendation to the user based on the difference in prices
pricediff=round(pred_price-price,2)
if pricediff>1:
    print("Since the option's traded price is significantly below its intrinsic value, we recommend to buy the option. The calculated price difference is: ",pricediff)
elif pricediff<-1:
    print("Since the option's traded price is significantly above its intrinsic value, we recommend to sell the option. The calculated price difference is: ",pricediff)
else: 
    print("There is no point in buying/selling this option due to the small difference between intrinsic and traded value and additional transaction costs.")
