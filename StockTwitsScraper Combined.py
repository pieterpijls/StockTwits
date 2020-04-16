# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Scrape seeking alpha!!

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen

data_ml = pd.read_excel('C:/Users/ppijls/Documents/R/Projects/Trading systems/StockTwits/TickersST.xlsx')
tickers = data_ml['ticker'].tolist()

followers = []

for i in range(0,len(tickers)):
    try:
        url = 'https://stocktwits.com/symbol/'+tickers[i]
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html')
    
        followers.append([i.text for i in soup.find_all(class_='st_HebiDD2 st_yCtClNI st_2mehCkH st_3PPn_WF')])
    except:
        followers.append(['0Watchers'])



# Datetime
from datetime import date
today = date.today()
d1 = today.strftime("%d-%m-%Y")

#
stocktwits_data = pd.DataFrame( 
    {'ticker': tickers,
     'followers': followers
    })

stocktwits_data['followers'] = stocktwits_data['followers'].astype(str).str[:-10].str[2:]
stocktwits_data['followers'] = stocktwits_data['followers'].str.replace(',', '')
stocktwits_data['followers'] = pd.to_numeric(stocktwits_data['followers'])



# Write to excel
stocktwits_data.to_excel("C:/Users/ppijls/Documents/R/Projects/Trading systems/StockTwits/stocktwitsoutput"+d1+".xlsx")



# Combine Files and create combined file
from datetime import date
start_date = date(2020, 3, 27)
today = date.today()
d1 = today.strftime("%d-%m-%Y")
d0 = start_date.strftime("%d-%m-%Y")

dates = pd.date_range(start = d0, end = d1)
dates = dates.strftime("%d-%m-%Y")

# read in all previous excel files
stocktwits = []

for i in range(0,len(dates)):
    try:
        tmp = pd.read_excel("C:/Users/ppijls/Documents/R/Projects/Trading systems/StockTwits/stocktwitsoutput"+dates[i]+".xlsx")
        tmp = tmp[['ticker','followers']]
        stocktwits.append(tmp)
    except:
        print('File on ' + dates[i] + ' is not available')

merged_df = pd.DataFrame(stocktwits[0])
merged_df = merged_df.rename(columns = {'followers':dates[0]})

for i in range(1,len(dates)): # start at 1 because already added first df
    try:
        merged_df = pd.merge(merged_df, stocktwits[i],  on = 'ticker')
        merged_df = merged_df.rename(columns = {'followers':dates[i+1]})  
    except:
        print('File on ' + dates[i] + ' is not available')

# Compute growth
merged_df['ST Growth'] = merged_df.iloc[:,-1]/merged_df.iloc[:,-2] - 1
merged_df['LT Growth'] = merged_df.iloc[:,-2]/merged_df.iloc[:,1] - 1

# Order by growth
merged_df = merged_df.sort_values(by = ['ST Growth'],ascending=False)

# Write to excel
merged_df.to_excel("C:/Users/ppijls/Documents/R/Projects/Trading systems/StockTwits/stocktwitsoutput combined"+d1+".xlsx")





