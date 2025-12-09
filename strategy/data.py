# Data Fetching Module
import yfinance as yf
import pandas as pd
import pandas_datareader.data as web
import numpy as np


def get_price_data(ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    """
    Downloads historical price data from yfinance.
    
    Parameters:
    -----------
    ticker : str
        Ticker symbol (e.g., "EURUSD=X" for FX pairs)
    start : str
        Start date in "YYYY-MM-DD" format
    end : str
        End date in "YYYY-MM-DD" format
    interval : str
        Data interval (default: "1d" for daily)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with 'Close' column and DateTimeIndex
    """
    df = yf.download(ticker, start=start, end=end, interval=interval, progress=False)

    # Handle multi-index columns if yfinance returns them
    if isinstance(df.columns, pd.MultiIndex):
        try:
            if 'Close' in df.columns.levels[0]:
                df = df['Close']
            else:
                df = df.iloc[:, 0].to_frame(name='Close')
        except:
            df = df.iloc[:, 0].to_frame(name='Close')
    else:
        if 'Close' in df.columns:
            df = df[['Close']]
        else:
            df = df.iloc[:, 0].to_frame(name='Close')

    # Ensure column is named 'Close'
    df.columns = ['Close'] if len(df.columns) == 1 else df.columns
    return df.dropna()


def get_macro_data(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches GDP and Current Account data for US and Euro Area from FRED.
    Creates a macro signal based on growth and trade differentials.
    
    Parameters:
    -----------
    start_date : str
        Start date in "YYYY-MM-DD" format
    end_date : str
        End date in "YYYY-MM-DD" format
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with 'Macro_Signal' column (1 = Bullish EUR, -1 = Bearish EUR)
    """
    print("Fetching Macro Data (GDP + Current Account)...")

    tickers = {
        'US_GDP': 'GDP',  # US GDP (Billions $)
        'EU_GDP': 'CLVMNACSCAB1GQEU28',  # Euro Area GDP (Real, Index)
        'US_CA': 'IEABC',  # US Current Account (Billions $)
        'EU_CA_Pct': 'EA19B6BLTT02STSAQ',  # Euro Area Current Account (% of GDP)
    }

    try:
        data = web.DataReader(list(tickers.values()), 'fred', start_date, end_date)
        data.columns = list(tickers.keys())
        data = data.resample('D').ffill()

        # Normalize data
        # GDP Growth (Year over Year using 252 trading days)
        data['US_Growth'] = data['US_GDP'].pct_change(252)
        data['EU_Growth'] = data['EU_GDP'].pct_change(252)

        # Current Account (Convert US to % of GDP to match EU)
        data['US_CA_Pct'] = (data['US_CA'] / data['US_GDP']) * 100

        # Calculate scores
        data['Growth_Diff'] = data['EU_Growth'] - data['US_Growth']
        data['Trade_Diff'] = data['EU_CA_Pct'] - data['US_CA_Pct']

        # Final signal (weighted sum)
        data['Total_Score'] = data['Growth_Diff'] + data['Trade_Diff']

        # Binary signal: 1 = Bullish EUR, -1 = Bearish EUR (Long USD)
        data['Macro_Signal'] = np.where(data['Total_Score'] > 0, 1, -1)

        print("Macro Data fetched successfully.")
        print(f"Signal Distribution:\n{data['Macro_Signal'].value_counts()}")

        return data[['Macro_Signal']]

    except Exception as e:
        print(f"Error fetching macro data: {e}")
        print("Using fallback signal (neutral: all 1s).")
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        return pd.DataFrame({'Macro_Signal': 1}, index=dates)

