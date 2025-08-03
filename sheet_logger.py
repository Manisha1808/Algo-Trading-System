import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from datetime import datetime
import requests

# Config
SHEET_NAME = "Algo Trading Log"
RESULTS_FOLDER = "backtest_results"
TELEGRAM_TOKEN = "7925030609:AAEwQS8_N9F7iZteNildjyE4ja1N0zypfGI"
TELEGRAM_CHAT_ID = "6167102552"

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Google Sheets connection
def connect_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

# Telegram message function
def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        logging.error(f"Failed to send message: {response.text}")

# Main function
def log_trades_to_sheet(results_folder, sheet_name="Algo Trading Log"):
    sheet = connect_sheet(sheet_name)
    trade_ws = sheet.worksheet("Trades")
    summary_ws = sheet.worksheet("Summary")

    all_trades = []
    for filename in os.listdir(results_folder):
        if filename.endswith("_trades.csv"):
            filepath = os.path.join(results_folder, filename)
            if os.stat(filepath).st_size == 0:
                logging.warning(f"{filename} is empty. Skipping.")
                continue
            try:
                df = pd.read_csv(filepath)
                if df.empty or df.columns.str.strip().tolist() == []:
                    logging.warning(f"{filename} has no data or columns. Skipping.")
                    continue
            except Exception as e:
                logging.error(f"Failed to read {filename}: {e}")
                continue

            ticker = filename.split("_")[0]
            df.columns = df.columns.str.strip()
            df["Ticker"] = ticker
            df["Buy Date"] = pd.to_datetime(df["Buy Date"])
            df["Sell Date"] = pd.to_datetime(df["Sell Date"])
            df["Holding Days"] = (df["Sell Date"] - df["Buy Date"]).dt.days
            df["Upload Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df["Buy Date"] = df["Buy Date"].dt.strftime("%Y-%m-%d")
            df["Sell Date"] = df["Sell Date"].dt.strftime("%Y-%m-%d")
            all_trades.append(df)

    if not all_trades:
        logging.warning("No trade data found.")
        return

    trades_df = pd.concat(all_trades, ignore_index=True)

    trade_ws.clear()
    trade_ws.append_row(trades_df.columns.tolist())
    for row in trades_df.values.tolist():
        trade_ws.append_row(row)
    logging.info("Trades uploaded to Google Sheet.")

    total_trades = len(trades_df)
    winning = trades_df[trades_df['P&L'] > 0]
    win_ratio = (len(winning) / total_trades) * 100
    total_pnl = trades_df['P&L'].sum()

    summary_ws.clear()
    summary_ws.append_row(["Total Trades", total_trades])
    summary_ws.append_row(["Winning Trades", len(winning)])
    summary_ws.append_row(["Win Ratio (%)", round(win_ratio, 2)])
    summary_ws.append_row(["Total P&L", round(total_pnl, 2)])
    logging.info("Summary stats uploaded.")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"""Trades uploaded to Google Sheet
Time: {timestamp}
Total Trades: {total_trades}
Winning Trades: {len(winning)}
Total P&L: {round(total_pnl, 2)}"""
    send_telegram_message(message)

if __name__ == "__main__":
    log_trades_to_sheet(RESULTS_FOLDER)
