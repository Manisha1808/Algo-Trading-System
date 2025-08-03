# Algo Trading System

## 📌 Project Overview
This project implements an **algorithmic trading system** using an **RSI and Moving Average crossover** strategy for selected **NIFTY 50 stocks** (RELIANCE, INFY, TCS). It performs:

- Data fetching via Yahoo Finance  
- Trade signal generation using a technical strategy  
- Backtesting over 6 months  
- Trade logging in Google Sheets  
- (Optional) ML-based price prediction  
- Telegram trade alerts (Bonus)

---

##  Strategy Logic

**Buy Signal when:**
- RSI < 30 (oversold)
- 20-DMA > 50-DMA (bullish crossover)

**Sell Logic:** Sell on the next available day after Buy.

---

##  Output & Deliverables

###  Console Output
- Strategy run logs
- Executed trades & P&L report
- ML model accuracy score (if enabled)

###  Google Sheets
- `Trades` tab: Trade-level logging
- `Summary` tab: Stats like win rate, total P&L

###  ML (Optional Bonus)
- Models: Logistic Regression & Random Forest
- Features: RSI, MACD, Volume, Volatility, ROC, 20DMA, 50DMA

---

## 📂 Folder Structure

```
algo_trading/
├── data_fetcher.py         # Fetches historical data using yfinance
├── strategy.py             # Implements RSI + MA crossover strategy
├── backtester.py           # Backtests trades, computes P&L
├── sheet_logger.py         # Logs trades & summary to Google Sheets
├── predictor.py            # ML model logic for forecasting
├── preprocess_data.py      # Feature engineering for ML
├── telegram_alert.py       # Sends trade alerts (placeholder)
├── main.py                 # Entry point for full pipeline
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Clone Repo or Unzip
```bash
git clone <your_repo_url>
cd algo_trading
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Full Pipeline
```bash
python main.py
```

---

## 🔗 External Services Used
- **Yahoo Finance API** (via `yfinance`)
- **Google Sheets API** (for logging trades)
- **Telegram Bot API** (for sending alerts - optional)

---

## 🔒 Security & Configuration Notice

This repository has been **sanitized** to protect sensitive credentials and personal configurations. To run this project end-to-end, replace the following:

### Google Sheets Credentials
- 🔒 File omitted: `credentials.json`
- Used for: Accessing and writing to your Google Sheet
- Action:
  - Create a Google Cloud project
  - Enable Sheets & Drive API
  - Download service account key (JSON)
  - Save it locally and update `sheet_logger.py`:
    ```python
    creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_credentials.json", scope)
    ```

### Telegram Bot Credentials
- 🔒 Placeholders used:
  ```python
  TELEGRAM_TOKEN = "bot_token_here"
  TELEGRAM_CHAT_ID = "chat_id_here"
  ```
- Used for: Sending Telegram alerts (bonus)
- Action:
  - Create a Telegram bot via [@BotFather](https://t.me/BotFather)
  - Replace placeholders in your `.py` file

### Google Sheet Access
- Sheet ID is **not hardcoded**.
- Ensure the Google Sheet (used for logging) has:
  - Two tabs: `Trades` and `Summary`
  - Editor access granted to your service account email

---

## 🔗 Links

- [ Google Drive Folder](https://drive.google.com/drive/u/0/folders/17KTbImy0Phtvi-CwtF4bsk3LKBuUB4Ye)
- [ GitHub Repository](https://github.com/Manisha1808/Algo-Trading-System)
- [ Google Sheet (View-Only Demo)](https://docs.google.com/spreadsheets/d/1khKzL75BP4E1Lot21dfdw17wXDObUDBNTHine62Scio/edit?usp=sharing)

> ⚠️ *The shared Google Sheet is for demo only. It contains mock data and is view-only. You may copy it and update credentials for personal use.*

---

## Author

**Manisha**  
*Feel free to connect for collaboration or questions.*
