# Binance Testnet Trading Bot — SMA Crossover

A simple Python trading bot that uses a **Simple Moving Average (SMA) crossover** strategy on Binance's testnet (fake money — no risk).

## How it works

- Fetches 1-hour candlestick data for BTCUSDT
- Calculates a **short SMA (7)** and a **long SMA (25)**
- **Buy signal**: short SMA crosses above long SMA (bullish)
- **Sell signal**: short SMA crosses below long SMA (bearish)
- Checks every 60 seconds and logs all decisions

## Setup

### 1. Get testnet API keys

1. Go to https://testnet.binance.vision/
2. Log in with GitHub
3. Click **Generate HMAC_SHA256 Key**
4. Copy the **API Key** and **Secret Key**

### 2. Add your keys

Open `config.py` and paste your keys:

```python
API_KEY = "your_api_key_here"
API_SECRET = "your_secret_key_here"
```

### 3. Install dependencies

```bash
pip install python-binance pandas
```

### 4. Run the bot

```bash
cd trading-bot
python bot.py
```

## Configuration

Edit the settings at the top of `bot.py`:

| Setting          | Default    | Description                      |
|------------------|------------|----------------------------------|
| `SYMBOL`         | `BTCUSDT`  | Trading pair                     |
| `SHORT_WINDOW`   | `7`        | Short SMA period (candles)       |
| `LONG_WINDOW`    | `25`       | Long SMA period (candles)        |
| `TRADE_QTY`      | `0.001`    | BTC amount per trade             |
| `CHECK_INTERVAL` | `60`       | Seconds between checks           |

## Stop the bot

Press **Ctrl+C** to gracefully shut down.
