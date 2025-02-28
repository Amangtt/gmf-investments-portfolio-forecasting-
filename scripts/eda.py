import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
from statsmodels.tsa.seasonal import seasonal_decompose

class analysis:

    def closing(df,ticker):
        
        df.set_index('Date', inplace=True)
        plt.figure(figsize=(10, 6))
        #Ploting closing price against date
        plt.plot(df.index,df['Close'], linestyle='-', color='b', label='Closing Price')
        plt.title(f'Closing Price Over Time for {ticker}', fontsize=16)
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)
        plt.legend()
        # Show the plot
        plt.tight_layout()
        plt.show()


    def precentage_change(df):
        #df.set_index('Date',inplace=True)
        # Calculating daily precentage change using Closing price
        df['Daily Change']=df['Close'].pct_change() * 100
        plt.figure(figsize=(10,6))
        plt.plot(df.index,df['Daily Change'],c='b')
        plt.xlabel('Date')
        plt.ylabel('Daily Percentage Change')
        plt.grid(True)
        plt.legend()
        plt.show()
   


    def rolling_avg(df):
        #df.set_index('Date',inplace=True)
        window_size=7
        # Rolling avg and standard deviation after each 7 days
        df['Rolling mean']=df['Close'].rolling(window=window_size).mean()
        df['Rolling std']=df['Close'].rolling(window=window_size).std()
        plt.figure(figsize=(12,8))
        plt.plot(df.index,df['Close'],label="Closing price",c='b')
        plt.plot(df.index,df['Rolling mean'],label=f'{window_size}-Day Rolling Mean',c='r')
        plt.plot(df.index,df['Rolling std'],label=f'{window_size}-Day Rolling std',c='g')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.legend()
        plt.show()


    
    def outliers(df):
        #df.set_index('Date', inplace=True)

        # Calculate daily returns (percentage change)
        df['Daily_Return'] = df['Close'].pct_change() * 100
        df.dropna(subset=['Daily_Return'], inplace=True)
        # Calculate Z-scores for daily returns
        df['Z_Score'] = zscore(df['Daily_Return'])
        
        # Define a threshold for outliers (e.g., Z-score > 3 or < -3)
        threshold = 3
        df['Outlier'] = np.abs(df['Z_Score']) > threshold

        # Identify days with unusually high or low returns
        outliers = df[df['Outlier']]

        # Plot daily returns and highlight outliers
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Daily_Return'], label='Daily Returns', color='b', alpha=0.7)
        plt.scatter(outliers.index, outliers['Daily_Return'], color='r', label='Outliers', zorder=5)
        plt.axhline(threshold, color='g', linestyle='--', label=f'Threshold (Z={threshold})')
        plt.axhline(-threshold, color='g', linestyle='--')

        plt.title('Daily Returns with Outliers Highlighted', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Daily Return (%)', fontsize=14)
        plt.grid(True)
        plt.legend()

        # Show the plot
        plt.tight_layout()
        plt.show()
        print("Days with Unusually High or Low Returns:")
        return outliers
    
    # Calculating var and shape ratio
    def var_sharpe(df):
        df['Daily_Return'] = df['Close'].pct_change() * 100
        confidence_level = 0.95
        VaR = np.percentile(df['Daily_Return'].dropna(), 100 * (1 - confidence_level))
        print(f'Value at Risk (VaR) at {confidence_level * 100}% confidence level: {VaR:.2f}%')
        risk_free_rate = 0  # Assume 0% risk-free rate for simplicity
        mean_daily_return = df['Daily_Return'].mean()
        std_daily_return = df['Daily_Return'].std()
        sharpe_ratio = (mean_daily_return - risk_free_rate) / std_daily_return

        print(f'Sharpe Ratio: {sharpe_ratio:.2f}')

    def decompose(df):
        #df.set_index('Date',inplace=True)
        
        decomposition=seasonal_decompose(df['Close'],model='additive',period=30)
        # After seasonal decomposition displays trend,seasonality and resid(Irregular components that the model couldn’t explain)
        plt.figure(figsize=(12, 8))
        plt.subplot(411)
        plt.plot(df.index,df["Close"], label="Original Time Series")
        plt.legend()

        plt.subplot(412)
        plt.plot(df.index,decomposition.trend, label="Trend", color="orange")
        plt.legend()

        plt.subplot(413)
        plt.plot(df.index,decomposition.seasonal, label="Seasonality", color="green")
        plt.legend()

        plt.subplot(414)
        plt.plot(df.index,decomposition.resid, label="Residuals", color="red")
        plt.legend()

        plt.tight_layout()
        plt.show()
