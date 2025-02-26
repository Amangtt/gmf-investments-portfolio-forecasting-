import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# TSLA   BND    SPY
def load_data(tickers,start_date,end_date):
    # The close column includes values with adj close 
    df=yf.download(tickers,start=start_date,end=end_date)
    df.reset_index(inplace=True)
    df.columns = df.columns.droplevel(1)
    return df
df=load_data('TSLA','2015-01-01','2025-01-31')

def stat(df):
    print(df.describe())
#stat(df)

def Inspect(df):
    inspection_results = {
            "data_types": df.dtypes,
            "missing_values": df.isnull().sum(),
            "duplicate_rows": df.duplicated().sum()
        }
    print(inspection_results)
#Inspect(df)

def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    print(df[(df[column] < lower_bound) | (df[column] > upper_bound)])  # Outliers

#detect_outliers_iqr(df, "Low")  # Example for stock price



def detect_outliers_with_boxplot(df,col):
           
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[col], color="skyblue")
    plt.title(f"Box Plot of {col}", fontsize=16)
    plt.xlabel(col, fontsize=14)
    plt.show()
detect_outliers_with_boxplot(df,'Volume')

