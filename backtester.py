# Updated backtest_strategy.py
import pandas as pd
import os
import logging

def backtest_strategy(df: pd.DataFrame, ticker: str):
    trades = []
    position = None

    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    for i in range(len(df) - 1):
        row = df.iloc[i]

        # Buy condition
        if row['RSI'] < 30 and row['20DMA'] > row['50DMA'] and position is None:
            buy_price = row['Close']
            buy_date = pd.to_datetime(row['Date'])
            position = {'buy_price': buy_price, 'buy_date': buy_date}
            logging.info(f"Buy signal on {buy_date.date()} at ₹{buy_price:.2f}")

        # Exit condition: hold for 5 days or last day
        elif position and ((pd.to_datetime(row['Date']) - position['buy_date']).days >= 5 or i == len(df) - 2):
            sell_price = row['Close']
            sell_date = pd.to_datetime(row['Date'])
            profit = sell_price - position['buy_price']
            trades.append({
                'Buy Date': position['buy_date'].date(),
                'Buy Price': position['buy_price'],
                'Sell Date': sell_date.date(),
                'Sell Price': sell_price,
                'P&L': profit
            })
            logging.info(f"Sell on {sell_date.date()} at ₹{sell_price:.2f} | P&L: ₹{profit:.2f}")
            position = None

    if not trades:
        logging.warning(f"No trades executed for {ticker}")
    else:
        logging.info(f"Completed backtest for {ticker} | Total trades: {len(trades)}")

    return pd.DataFrame(trades)


# Updated main.py
import os
import logging
import pandas as pd
from datetime import datetime, timedelta
from data_fetcher import fetch_data
from strategy import apply_strategy
from backtester import backtest_strategy
from sheet_logger import log_trades_to_sheet

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
STOCKS = ["RELIANCE.NS", "INFY.NS", "TCS.NS"]
END_DATE = datetime.today().date()
START_DATE = END_DATE - timedelta(days=180)
RESULTS_FOLDER = "backtest_results"


def main():
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    for symbol in STOCKS:
        logging.info(f"Running strategy for {symbol}")
        logging.info(f"Fetching data for {symbol} from {START_DATE} to {END_DATE}")

        df = fetch_data(symbol, START_DATE, END_DATE)
        if df.empty:
            logging.warning(f"No data found for {symbol}. Skipping...")
            continue

        df.reset_index(inplace=True)
        df = apply_strategy(df)

        trades_df = backtest_strategy(df, symbol)

        trades_file = os.path.join(RESULTS_FOLDER, f"{symbol}_trades.csv")
        trades_df.to_csv(trades_file, index=False)
        logging.info(f"Saved trades for {symbol} to {trades_file}")

    log_trades_to_sheet(results_folder=RESULTS_FOLDER)


if __name__ == "__main__":
    main()
