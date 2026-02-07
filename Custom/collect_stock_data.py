import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Calculate date from 6 years ago
end_date = datetime.now()
start_date = end_date - timedelta(days=6*365)

# Our selected 10 ETFs
symbols = ['SPY', 'QQQ', 'XLF', 'XLE', 'XLV', 'XLP', 'XLRE', 'VIG', 'AGG', 'GLD']

# Create an empty DataFrame to store closing prices
all_data = pd.DataFrame()

# Get monthly closing prices for each ETF
for symbol in symbols:
    print(f"Getting historical data for {symbol}...")
    
    try:
        # Use yfinance to get monthly data
        data = yf.download(symbol, start=start_date, end=end_date, interval='1mo')
        
        # Extract closing prices
        close_prices = data['Close']
        
        # Rename column and add to total dataframe
        close_prices.name = symbol
        
        # Merge data
        if all_data.empty:
            all_data = pd.DataFrame(close_prices)
        else:
            all_data = all_data.join(close_prices, how='outer')
        
        # Avoid too frequent API requests
        time.sleep(1)
        
    except Exception as e:
        print(f"Error getting data for {symbol}: {e}")

# Fill missing values (if any)
all_data = all_data.fillna(method='ffill')

# Save as text file, format same as original file
header = "#" + "\t".join(symbols)
np.savetxt('StockHistory-10-Custom.txt', all_data.values, delimiter='\t', header=header, comments='')

print("Data collection complete, saved to StockHistory-10-Custom.txt")

# Get annual dividend data
print("\nGetting annual dividend data...")
dividends = []

for symbol in symbols:
    try:
        # Get stock information
        stock = yf.Ticker(symbol)
        
        # Try to get dividend yield
        try:
            div_yield = stock.info.get('dividendYield', 0)
            if div_yield is None:
                div_yield = 0
        except:
            div_yield = 0
            
        dividends.append(div_yield)
        print(f"Estimated annual dividend rate for {symbol}: {div_yield:.4f}")
        
    except Exception as e:
        print(f"Error getting dividend data for {symbol}: {e}")
        dividends.append(0.01)  # Default value

print("\nDividend data list:")
print(dividends)
print("\nFormat for Python code:")
print(f"StockDividend = {dividends}")
