import yfinance as yf
import pandas as pd
import numpy as np
import logging
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
print("Script started.")

def calculate_indicators(df):
    df['Return'] = df['Close'].pct_change()

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Additional features
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    df['Volatility'] = df['Close'].rolling(window=10).std()
    df['ROC'] = df['Close'].pct_change(periods=5)

    # Define target: 1 if next day's return is positive, else 0
    df['Target'] = (df['Return'].shift(-1) > 0).astype(int)

    return df

def train_model(df):
    features = ['RSI', 'MACD', 'Volume', '20DMA', '50DMA', 'Volatility', 'ROC']
    expected_cols = features + ['Target']

    df = df.dropna(subset=expected_cols)
    logging.info(f"Final dataset shape: {df.shape}")

    # Handle class imbalance
    df_model = df[expected_cols]
    df_majority = df_model[df_model['Target'] == 0]
    df_minority = df_model[df_model['Target'] == 1]

    df_minority_upsampled = resample(df_minority, replace=True, n_samples=len(df_majority), random_state=42)
    df_balanced = pd.concat([df_majority, df_minority_upsampled])

    X = df_balanced[features]
    y = df_balanced['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Logistic Regression
    logging.info("Training Logistic Regression model...")
    log_model = LogisticRegression(max_iter=1000)
    log_model.fit(X_train, y_train)
    y_pred_log = log_model.predict(X_test)

    acc_log = accuracy_score(y_test, y_pred_log)
    print(f"\nLogistic Regression Accuracy: {acc_log:.2f}")
    print(classification_report(y_test, y_pred_log))

    # Random Forest
    logging.info("Training Random Forest model...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)

    acc_rf = accuracy_score(y_test, y_pred_rf)
    print(f"\nRandom Forest Accuracy: {acc_rf:.2f}")
    print(classification_report(y_test, y_pred_rf))

    return log_model, rf_model

def main():
    ticker = "INFY.NS"
    logging.info(f"Downloading historical data for {ticker}...")
    df = yf.download(ticker, period='2y', interval='1d')

    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = calculate_indicators(df)

    print("Feature columns after indicator calculation:")
    print(df.columns.tolist())

    train_model(df)

if __name__ == "__main__":
    main()
