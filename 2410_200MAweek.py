# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 18:30:14 2024

@author: Vittorio
"""

import yfinance as yf
import pandas as pd
 

file_path = r'C:\Users\Utente1\Documents\Python Scripts\files\mi_piacciono.txt'


with open(file_path, 'r') as file:
    tickers = [line.strip() for line in file.readlines()]


def calculate_200w_ma_distance(ticker):
    # Download stock data with weekly frequency
    data = yf.download(ticker, period='max', interval='1wk', progress='false')
    
    # Calculate the 200-week moving average (200W MA)
    data['200W_MA'] = data['Adj Close'].rolling(window=200).mean()
    
    # Get the latest price and the latest 200W MA
    current_price = data['Adj Close'].iloc[-1]
    ma_200 = data['200W_MA'].iloc[-1]
    
    # Calculate the percentage distance from the 200W MA
    distance_percent = ((current_price - ma_200) / ma_200) * 100
    
    return ticker, current_price, ma_200, distance_percent


# Create a list to store the results
results = []


# Loop through each ticker and calculate the 200W MA distance
for ticker in tickers:
    try:
        ticker, current_price, ma_200, distance_percent = calculate_200w_ma_distance(ticker)
        results.append((ticker, current_price, ma_200, distance_percent))
    except Exception as e:
        print(f"Could not process {ticker}: {e}")


# Create a DataFrame to display the results
df_results = pd.DataFrame(results, columns=['Ticker', 'Current Price', '200W MA', 'Distance (%)'])


# Display the results
print()
print(df_results)


# Optionally, save the results to a CSV file
#df_results.to_csv(r'C:\Users\Utente1\Documents\Python Scripts\files\200w_ma_distance_results.csv', index=False)

