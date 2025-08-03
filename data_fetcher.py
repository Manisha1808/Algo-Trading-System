import yfinance as yf
import pandas as pd

def fetch_data(symbol, start_date, end_date):
    print(f"Fetching data for {symbol} from {start_date} to {end_date}")
    
    data = yf.download(symbol, start=start_date, end=end_date, progress=False)

    # Flatten MultiIndex if it exists
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    
    if 'Close' in data.columns and isinstance(data['Close'], pd.DataFrame):
        data['Close'] = data['Close'].iloc[:, 0]
    elif isinstance(data['Close'], pd.Series):
        data['Close'] = data['Close']
    else:
        data['Close'] = pd.Series(data['Close'])

    data.dropna(inplace=True)
    return data
