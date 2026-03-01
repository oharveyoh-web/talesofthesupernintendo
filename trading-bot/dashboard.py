import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows encoding issues
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from binance.client import Client

from config import API_KEY, API_SECRET, BASE_URL

HISTORY_FILE = Path(__file__).parent / "portfolio_history.json"

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT",
    "POLUSDT", "LTCUSDT", "FIOUSDT", "STEEMUSDT", "COSUSDT",
]

REFRESH = 5  # seconds between refreshes


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return []


def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history))


def add_snapshot(history, total_usdt):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({"time": now, "value": round(total_usdt, 2)})
    # Keep last 1440 entries (~24h at 1/min)
    if len(history) > 1440:
        history = history[-1440:]
    save_history(history)
    return history


def run():
    client = Client(API_KEY, API_SECRET, testnet=True)
    client.API_URL = BASE_URL + "/api"
    history = load_history()

    while True:
        clear()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ── Account balances ──────────────────────────────
        account = client.get_account()
        balances = [b for b in account["balances"]
                    if (float(b["free"]) > 0 or float(b["locked"]) > 0)
                    and b["asset"].isascii()]

        print("=" * 70)
        print(f"  TRADING BOT DASHBOARD                          {now}")
        print("=" * 70)

        print("\n  BALANCES")
        print(f"  {'Asset':<10} {'Free':>16} {'Locked':>16}")
        print("  " + "-" * 42)
        for b in balances:
            print(f"  {b['asset']:<10} {float(b['free']):>16.6f} {float(b['locked']):>16.6f}")

        # ── Live prices & 24h change ─────────────────────
        tickers = {t["symbol"]: t for t in client.get_ticker()}

        print(f"\n  MARKET OVERVIEW ({len(SYMBOLS)} pairs)")
        print(f"  {'Pair':<12} {'Price':>14} {'24h Change':>12} {'Volume (USDT)':>16}")
        print("  " + "-" * 56)
        for sym in SYMBOLS:
            t = tickers.get(sym)
            if not t:
                print(f"  {sym:<12} {'N/A':>14}")
                continue
            price = float(t["lastPrice"])
            pct = float(t["priceChangePercent"])
            vol = float(t["quoteVolume"])
            sign = "+" if pct >= 0 else ""
            arrow = "^" if pct >= 0 else "v"
            print(f"  {sym:<12} {price:>14.4f} {sign}{pct:>7.2f}% {arrow}  {vol:>14.0f}")

        # ── Recent orders ────────────────────────────────
        print(f"\n  RECENT ORDERS")
        print(f"  {'Time':<20} {'Pair':<12} {'Side':<6} {'Qty':>12} {'Status':<10}")
        print("  " + "-" * 62)

        all_orders = []
        for sym in SYMBOLS:
            try:
                orders = client.get_all_orders(symbol=sym, limit=5)
                all_orders.extend(orders)
            except Exception:
                pass

        # Sort by time, most recent first
        all_orders.sort(key=lambda o: o["time"], reverse=True)

        if not all_orders:
            print("  No orders yet. Waiting for signals...")
        else:
            for o in all_orders[:20]:
                t = datetime.fromtimestamp(o["time"] / 1000, tz=timezone.utc)
                ts = t.strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {ts:<20} {o['symbol']:<12} {o['side']:<6} {o['executedQty']:>12} {o['status']:<10}")

        # ── P&L estimate ─────────────────────────────────
        total_usdt = 0.0
        for b in balances:
            asset = b["asset"]
            free = float(b["free"]) + float(b["locked"])
            if asset == "USDT":
                total_usdt += free
            else:
                ticker = tickers.get(asset + "USDT")
                if ticker:
                    total_usdt += free * float(ticker["lastPrice"])

        history = add_snapshot(history, total_usdt)

        print(f"\n  PORTFOLIO VALUE: ~${total_usdt:,.2f}")

        # ── Portfolio history ────────────────────────────
        print(f"\n  PORTFOLIO HISTORY (last 20 snapshots)")
        print(f"  {'Time':<20} {'Value (USDT)':>14} {'Change':>10}")
        print("  " + "-" * 46)

        recent = history[-20:]
        first_value = history[0]["value"] if history else total_usdt
        for i, snap in enumerate(recent):
            val = snap["value"]
            if i == 0 and len(history) > len(recent):
                prev_val = history[-(len(recent) + 1)]["value"]
            elif i == 0:
                prev_val = val
            else:
                prev_val = recent[i - 1]["value"]
            diff = val - prev_val
            sign = "+" if diff >= 0 else ""
            print(f"  {snap['time']:<20} ${val:>12,.2f}  {sign}{diff:>8,.2f}")

        # Overall change since tracking started
        overall = total_usdt - first_value
        overall_sign = "+" if overall >= 0 else ""
        print(f"\n  Since tracking started: {overall_sign}${overall:,.2f}")

        print("\n  " + "-" * 56)
        print(f"  Refreshing every {REFRESH}s  |  Press Ctrl+C to exit")
        print("=" * 70)

        time.sleep(REFRESH)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nDashboard closed.")
