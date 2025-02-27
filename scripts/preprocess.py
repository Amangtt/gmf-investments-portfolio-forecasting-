import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# TSLA   BND    SPY
class cleaning:
    def load_data(tickers,start_date,end_date):
        # The close column includes values with adj close 
        df=yf.download(tickers,start=start_date,end=end_date)
        df.reset_index(inplace=True)
        df.columns = df.columns.droplevel(1)
        df.to_csv(f'../Data/{tickers}.csv', index=False)
        return df
   

    def stat(df):
        # Description on dataset
        return df.describe()
    #stat(df)

    def Inspect(df):
        # Information about the datas
        inspection_results = {
                "data_types": df.dtypes,
                "missing_values": df.isnull().sum(),
                "duplicate_rows": df.duplicated().sum()
            }
        return inspection_results
    

    def detect_outliers_iqr(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return df[(df[column] < lower_bound) | (df[column] > upper_bound)]  # Outliers

    


    # Detecting outliers with vizualization using box plot
    def detect_outliers_with_boxplot(df,col):
            
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=df[col], color="skyblue")
        plt.title(f"Box Plot of {col}", fontsize=16)
        plt.xlabel(col, fontsize=14)
        plt.show()
  

