Group project #2258: european option pricing with python

**About**

This is a student project of the university of St. Gallen of the course Programming with Advanced Computer Languages. Our goal is to provide the user 
a basic recommendation on investing in an european option by calculating the real option value and comparing it to the currently traded price.

**Pre-requisites**

The program works with Python3.9
In order to run it, the following libraries/modules need to be installed:
yfinance, numpy, math, pandas, datetime, relativedelta

**Instructions**

1. Start european_option_pricing.py
2. Follow the programmes’ instructions and input the following data points.
	2.1 The stock’s ticker
	2.2 The expiration date
	2.3 The option type (put / call)
	2.4 The strike price
3. Enjoy our recommendation


**Description**

What did we do?
Through our program, users can compare real market prices of european stock options with the options’ intrinsic value calculated through the binomial method. 
In the beginning all necessary libraries - yfinance, numpy, math, pandas, datetime, relativedelta - were installed. Then the program requires the user to input information to determine which option the user wants. First the stock’s ticker to determine the company, then the expiration date based on a list provided by the program. Afterwards the user needs to decide if he wants a put or call option and a strike price. Basic information on options can be found at the end of this document.
The next step is the definition of four functions for the different option types: european call options, european call options with dividends, european put options and european put options with dividends. The functions are based on the binomial pricing model and provide the intrinsic value of the option using 50 iterations.
At the end the program chooses the function which fits to the user input and provides a small recommendation to the user if there is a significant difference between the intrinsic option price and the currently traded price.

What are european stock options?
An european stock option gives the holder the right (but not the obligation) to buy or sell the underlying stock in the future at a price that is already fixed today. The right to buy / sell the underlying is termed call / put. The in advance fixed price to buy/sell the underlying is called strike price. 

What is a binomial option pricing model?
We use a binomial model approach to approximate option prices. The binomial option pricing model uses an iterative procedure, allowing for the specification of nodes (points in time) during the time span between the valuation date and the option's expiration date. A binomial model can be visualized graphically by a binomial tree. The binomial tree consists of possible intrinsic values that an option may take at different nodes or time periods. The number n determines the number of iterations between today and the expiration date of the option.


**Sources**

https://github.com/ranaroussi/yfinance

Hull, J.C. (2012). Options, Futures and Other Derivatives. 8th Edition, Prentice-Hall, Upper Saddle River. pp. 253-273

https://www.investopedia.com/articles/investing/021215/examples-understand-binomial-option-pricing-model.asp
