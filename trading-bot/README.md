# Binance Testnet Trading Bot — Multi-Pair SMA Crossover Scanner

A Python trading bot that uses a **Simple Moving Average (SMA) crossover** strategy to scan multiple cryptocurrency pairs on Binance's testnet (fake money — no risk). Includes a live terminal dashboard for monitoring balances, prices, orders, and portfolio history.

## How it works

- Scans **15 trading pairs** every 2 seconds using 1-minute candlestick data
- Calculates a **short SMA (5)** and a **long SMA (50)** for each pair
- **Buy signal**: short SMA crosses above long SMA (bullish crossover)
- **Sell signal**: short SMA crosses below long SMA (bearish crossover)
- Tracks position state per symbol to avoid duplicate entries
- Logs all decisions with timestamps

### Supported pairs

BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT, DOGEUSDT, ADAUSDT, AVAXUSDT, DOTUSDT, LINKUSDT, POLUSDT, LTCUSDT, FIOUSDT, STEEMUSDT, COSUSDT

## Project structure

```
trading-bot/
├── bot.py                  # Main trading bot (SMA crossover scanner)
├── dashboard.py            # Live terminal dashboard
├── config.py               # API keys and base URL
├── portfolio_history.json  # Auto-generated portfolio value snapshots
└── README.md
```

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
BASE_URL = "https://testnet.binance.vision"
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

### 5. Run the dashboard (optional)

In a separate terminal:

```bash
cd trading-bot
python dashboard.py
```

## Dashboard

The dashboard (`dashboard.py`) provides a live terminal view that refreshes every 5 seconds:

- **Balances** — current holdings (free and locked)
- **Market overview** — live prices and 24h change for all 15 pairs
- **Recent orders** — last 20 orders across all pairs
- **Portfolio value** — estimated total value in USDT
- **Portfolio history** — tracks value over time (up to 1440 snapshots / ~24h)

## Configuration

### Bot settings (top of `bot.py`)

| Setting          | Default     | Description                          |
|------------------|-------------|--------------------------------------|
| `SYMBOLS`        | 15 pairs    | List of trading pairs to scan        |
| `SHORT_WINDOW`   | `5`         | Short SMA period (candles)           |
| `LONG_WINDOW`    | `50`        | Long SMA period (candles)            |
| `KLINE_INTERVAL` | `1 minute`  | Candlestick interval                 |
| `CHECK_INTERVAL` | `2`         | Seconds between full scans           |
| `TRADE_QTYS`     | per-symbol  | Trade quantity map (see `bot.py`)    |
| `DEFAULT_QTY`    | `1.0`       | Fallback quantity for unlisted pairs |

### Dashboard settings (top of `dashboard.py`)

| Setting   | Default | Description                  |
|-----------|---------|------------------------------|
| `REFRESH` | `5`     | Seconds between refreshes    |

## Stop the bot

Press **Ctrl+C** to gracefully shut down either the bot or the dashboard.
