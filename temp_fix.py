from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
y_symbols = ['HDFCBANK.NS']
from datetime import datetime
startdate = datetime(2022,12,1)
enddate = datetime(2022,12,15)
data = pdr.get_data_yahoo(y_symbols, start=startdate, end=enddate)
print(data)