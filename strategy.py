import pandas as pd
import ta

def add_indicators(df):
    # Ensure Close is clean
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate RSI
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

    # Calculate moving averages
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()

    df.dropna(inplace=True)
    return df

def apply_strategy(df):
    df = add_indicators(df)
    df['Signal'] = 0

    condition = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
    print("Total rows:", len(df))
    print("Rows where RSI < 30:", (df['RSI'] < 30).sum())
    print("Rows where 20DMA > 50DMA:", (df['20DMA'] > df['50DMA']).sum())
    print("Rows where both conditions met:", condition.sum())

    df.loc[condition, 'Signal'] = 1
    return df
