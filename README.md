# Algo Trading System 

## 📌 Project Overview
This project implements an **algorithmic trading system** using **RSI and Moving Average crossover** strategy for selected **NIFTY 50 stocks** (RELIANCE, INFY, TCS). It performs:

- Data fetching via Yahoo Finance
- Trade signal generation using a technical strategy
- Backtesting over 6 months
- Trade logging in Google Sheets
- (Optional) ML-based price prediction
- Telegram trade alerts (Bonus)

---

##  Strategy Logic
The **Buy Signal** is triggered when:
- **RSI < 30** (oversold)
- **20-DMA > 50-DMA** (bullish trend)

**Sell Logic:** Sell on the next available day.

---

##  Output & Deliverables

### Console Output
- Strategy logs
- Trades executed and P&L
- ML model accuracy

### Google Sheets
- Trades logged in `Trades` tab
- Summary in `Stats` tab

### ML (Optional Bonus)
- Logistic Regression & Random Forest used to predict next-day price movement using:
  - RSI, MACD, Volume, ROC, Volatility, 20DMA, 50DMA

---

## 📂 Folder Structure

```
algo_trading/
├── data_fetcher.py          # Fetches data from Yahoo Finance
├── strategy.py              # RSI + MA crossover logic
├── backtester.py            # Backtests signals, computes P&L
├── sheet_logger.py          # Logs trades and stats to Google Sheets
├── telegram_bot.py          # Sends alerts (bonus)
├── ml_model.py              # ML prediction using Logistic/Random Forest
├── main.py                  # Auto-runs full pipeline
├── requirements.txt
└── README.md
```

---

##  How to Run

### 1. Clone Repo or Unzip
```bash
git clone <repo-url>  # or unzip the folder
cd algo_trading
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Full Pipeline
```bash
python main.py
```

---

## 🔗 External Services Used
- **Yahoo Finance API** (via `yfinance`)
- **Google Sheets API** (for trade logs)
- **Telegram Bot API** (for alerts, optional)

---


Available in the shared Google Drive folder.

---

## 🔗 Links
- [Google Drive Folder](<https://drive.google.com/drive/u/0/folders/17KTbImy0Phtvi-CwtF4bsk3LKBuUB4Ye>)
- [GitHub Repository](<https://github.com/Manisha1808/Algo-Trading-System>)
- [Google Sheets](<https://docs.google.com/spreadsheets/d/1khKzL75BP4E1Lot21dfdw17wXDObUDBNTHine62Scio/edit?usp=sharing>)
---




## Author
**Manisha**  
Feel free to contact for queries or improvements.
