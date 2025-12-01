import yfinance as yf
import pandas as pd
import numpy as np

# ----------------------------------------
# Fetch price data safely
# ----------------------------------------
def get_price_series(symbol: str, period="6mo"):
    try:
        df = yf.download(symbol, period=period, interval="1d", progress=False)

        if df is None or df.empty:
            print(f"[ERROR] No data for {symbol}")
            return None

        df = df.dropna()
        return df

    except Exception as e:
        print(f"[ERROR] yfinance failed for {symbol}: {e}")
        return None


# ----------------------------------------
# SMA indicator
# ----------------------------------------
def simple_moving_average(df, window):
    return df["Close"].rolling(window=window).mean()


# ----------------------------------------
# RSI indicator (safe version)
# ----------------------------------------
def compute_rsi(df, period=14):
    try:
        delta = df["Close"].diff()

        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        roll_up = pd.Series(gain).rolling(period).mean()
        roll_down = pd.Series(loss).rolling(period).mean()

        rs = roll_up / (roll_down + 1e-9)
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]
    except Exception as e:
        print(f"[ERROR] RSI failed: {e}")
        return None


# ----------------------------------------
# MACD indicator
# ----------------------------------------
def compute_macd(df):
    try:
        short = df["Close"].ewm(span=12, adjust=False).mean()
        long = df["Close"].ewm(span=26, adjust=False).mean()
        macd = short - long
        signal = macd.ewm(span=9, adjust=False).mean()

        return macd.iloc[-1], signal.iloc[-1]
    except Exception as e:
        print(f"[ERROR] MACD failed: {e}")
        return None, None


# ----------------------------------------
# ADVANCED SIGNAL ENGINE
# ----------------------------------------
def advanced_signal(symbol: str):
    df = get_price_series(symbol)

    if df is None:
        return "ERROR"

    try:
        sma20 = simple_moving_average(df, 20).iloc[-1]
        sma50 = simple_moving_average(df, 50).iloc[-1]
        rsi = compute_rsi(df)
        macd, macd_signal = compute_macd(df)

        # Safety: Any missing value → HOLD
        if any(v is None for v in [sma20, sma50, rsi, macd, macd_signal]):
            print(f"[WARN] Missing indicator for {symbol}")
            return "HOLD"

        # ----------------------------------
        # BUY CONDITIONS
        # ----------------------------------
        if sma20 > sma50 and rsi < 70 and macd > macd_signal:
            return "BUY"

        # ----------------------------------
        # SELL CONDITIONS
        # ----------------------------------
        if sma20 < sma50 and rsi > 30 and macd < macd_signal:
            return "SELL"

        return "HOLD"

    except Exception as e:
        print(f"[ERROR] Signal failed for {symbol}: {e}")
        return "ERROR"
