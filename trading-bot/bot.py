import time
from datetime import datetime

import pandas as pd
from binance.client import Client

from config import API_KEY, API_SECRET, BASE_URL

# ── Settings ──────────────────────────────────────────────
SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "DOGEUSDT",
    "ADAUSDT",
    "AVAXUSDT",
    "DOTUSDT",
    "LINKUSDT",
    "POLUSDT",
    "LTCUSDT",
    "FIOUSDT",
    "STEEMUSDT",
    "COSUSDT",
]

SHORT_WINDOW = 5       # Short SMA period (candles)
LONG_WINDOW = 50       # Long SMA period (candles)
KLINE_INTERVAL = Client.KLINE_INTERVAL_1MINUTE
CHECK_INTERVAL = 2     # Seconds between full scans

# Trade quantity per symbol (adjust per coin's price)
TRADE_QTYS = {
    "BTCUSDT":   0.001,
    "ETHUSDT":   0.01,
    "BNBUSDT":   0.1,
    "SOLUSDT":   0.1,
    "XRPUSDT":   10.0,
    "DOGEUSDT":  50.0,
    "ADAUSDT":   20.0,
    "AVAXUSDT":  0.5,
    "DOTUSDT":   1.0,
    "LINKUSDT":  1.0,
    "POLUSDT": 20.0,
    "LTCUSDT":   0.1,
    "FIOUSDT":   100.0,
    "STEEMUSDT": 50.0,
    "COSUSDT":   100.0,
}
DEFAULT_QTY = 1.0  # Fallback if symbol not in TRADE_QTYS


def connect(api_key, api_secret, base_url):
    client = Client(api_key, api_secret, testnet=True)
    client.API_URL = base_url + "/api"
    account = client.get_account()
    print(f"[OK] Connected to Binance testnet  |  Status: {account['accountType']}")
    return client


def fetch_candles(client, symbol, interval, limit):
    raw = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(raw, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_vol", "trades", "taker_buy_base",
        "taker_buy_quote", "ignore",
    ])
    df["close"] = pd.to_numeric(df["close"])
    return df


def compute_smas(df, short_window, long_window):
    df["sma_short"] = df["close"].rolling(window=short_window).mean()
    df["sma_long"] = df["close"].rolling(window=long_window).mean()
    return df


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}]  {msg}")


def run():
    print("=" * 65)
    print("  Binance Testnet Bot — Multi-Pair SMA Crossover Scanner")
    print("=" * 65)
    print(f"  Scanning {len(SYMBOLS)} pairs  |  SMA {SHORT_WINDOW}/{LONG_WINDOW}  |  Every {CHECK_INTERVAL}s")
    print(f"  Pairs: {', '.join(SYMBOLS)}")
    print("=" * 65)

    client = connect(API_KEY, API_SECRET, BASE_URL)

    # Track position per symbol
    positions = {s: False for s in SYMBOLS}

    while True:
        log(f"--- Scanning {len(SYMBOLS)} pairs ---")

        for symbol in SYMBOLS:
            try:
                df = fetch_candles(client, symbol, KLINE_INTERVAL, limit=LONG_WINDOW + 5)
                df = compute_smas(df, SHORT_WINDOW, LONG_WINDOW)

                latest = df.iloc[-1]
                prev = df.iloc[-2]
                price = latest["close"]
                sma_s = latest["sma_short"]
                sma_l = latest["sma_long"]

                cross_up = prev["sma_short"] <= prev["sma_long"] and sma_s > sma_l
                cross_down = prev["sma_short"] >= prev["sma_long"] and sma_s < sma_l

                qty = TRADE_QTYS.get(symbol, DEFAULT_QTY)

                if cross_up and not positions[symbol]:
                    log(f">>> BUY  {symbol}  |  Price: {price:.4f}  |  SMA-{SHORT_WINDOW}: {sma_s:.4f} > SMA-{LONG_WINDOW}: {sma_l:.4f}")
                    order = client.order_market_buy(symbol=symbol, quantity=qty)
                    log(f"    Order: {order['side']} {order['executedQty']} {symbol}  |  Status: {order['status']}")
                    positions[symbol] = True

                elif cross_down and positions[symbol]:
                    log(f">>> SELL {symbol}  |  Price: {price:.4f}  |  SMA-{SHORT_WINDOW}: {sma_s:.4f} < SMA-{LONG_WINDOW}: {sma_l:.4f}")
                    order = client.order_market_sell(symbol=symbol, quantity=qty)
                    log(f"    Order: {order['side']} {order['executedQty']} {symbol}  |  Status: {order['status']}")
                    positions[symbol] = False

                else:
                    state = "HOLD" if positions[symbol] else "---"
                    log(f"    {symbol:<12} Price: {price:.4f}  |  SMA-{SHORT_WINDOW}: {sma_s:.4f}  |  SMA-{LONG_WINDOW}: {sma_l:.4f}  [{state}]")

            except Exception as e:
                log(f"    {symbol:<12} [ERROR] {e}")

        log(f"--- Scan complete. Sleeping {CHECK_INTERVAL}s ---\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nBot stopped by user (Ctrl+C). Goodbye!")
