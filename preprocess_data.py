import yfinance as yf
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def preprocess_and_save(ticker):
    logging.info(f"Downloading data for {ticker}...")
    df = yf.download(ticker, period='6mo', interval='1d', auto_adjust=True, progress=False)

    if df.empty:
        logging.warning(f"No data returned for {ticker}")
        return

    # Flatten multi-indexed columns, if any
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    logging.info(f"Columns after download: {df.columns.tolist()}")

    if 'Close' not in df.columns:
        logging.error(f"'Close' column missing in data for {ticker}")
        return

    # Compute technical indicators
    df['RSI'] = compute_rsi(df['Close'])
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()

    indicator_cols = ['RSI', '20DMA', '50DMA']
    missing_cols = [col for col in indicator_cols if col not in df.columns]

    if missing_cols:
        logging.error(f"Missing expected columns: {missing_cols}")
        return

    logging.info(f"Null values — RSI: {df['RSI'].isna().sum()}, 20DMA: {df['20DMA'].isna().sum()}, 50DMA: {df['50DMA'].isna().sum()}")

    df.dropna(subset=indicator_cols, inplace=True)
    df.reset_index(inplace=True)

    os.makedirs("processed_data", exist_ok=True)
    file_path = f"processed_data/{ticker.split('.')[0]}.csv"
    df.to_csv(file_path, index=False)
    logging.info(f"Saved processed data to {file_path}")

if __name__ == "__main__":
    tickers = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS']
    for ticker in tickers:
        try:
            preprocess_and_save(ticker)
        except Exception as e:
            logging.error(f"Error processing {ticker}: {e}")
