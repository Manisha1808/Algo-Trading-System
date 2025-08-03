import os
import logging
import pandas as pd
from datetime import datetime, timedelta
from data_fetcher import fetch_data
from strategy import apply_strategy
from backtester import backtest_strategy
from sheet_logger import log_trades_to_sheet

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
        results = backtest_strategy(df, symbol)

        if isinstance(results, list):
            results = pd.DataFrame(results)

        results_file = os.path.join(RESULTS_FOLDER, f"{symbol}_results.csv")
        trades_file = os.path.join(RESULTS_FOLDER, f"{symbol}_trades.csv")

        results.to_csv(results_file, index=False)
        
        # Fix: Always create CSV with headers even if empty
        trade_columns = ['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'P&L']
        if 'Buy Date' in results.columns and not results.empty:
            trades = results[['Buy Date', 'Buy Price', 'Sell Date', 'Sell Price', 'P&L']].copy()
            if trades.empty:
                trades = pd.DataFrame(columns=trade_columns)
        else:
            trades = pd.DataFrame(columns=trade_columns)

        trades.to_csv(trades_file, index=False)
        logging.info(f"Saved trades for {symbol} to {trades_file}")
        logging.info(f"Saved results for {symbol} to {results_file}")

    log_trades_to_sheet(results_folder=RESULTS_FOLDER)

if __name__ == "__main__":
    main()
