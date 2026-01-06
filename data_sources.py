import requests
import pandas as pd
import time
from datetime import datetime, timedelta

BINANCE_BASE = "https://api.binance.com/api/v3/klines"
COINGECKO_BASE = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"


def get_binance_symbol(symbol: str) -> str:
    """
    Convert a symbol like 'BTC' → 'BTCUSDT'
    """
    return f"{symbol.upper()}USDT"


def fetch_binance_ohlcv(symbol: str, interval: str, days: int = 90):
    """
    Fetch OHLCV data from Binance public API.
    Returns a pandas DataFrame or None if Binance fails.
    """
    try:
        end_time = int(time.time() * 1000)
        start_time = end_time - (days * 24 * 60 * 60 * 1000)

        params = {
            "symbol": get_binance_symbol(symbol),
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1500
        }

        r = requests.get(BINANCE_BASE, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])

        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        df["date"] = pd.to_datetime(df["open_time"], unit="ms")

        return df[["date", "open", "high", "low", "close", "volume"]]

    except Exception:
        return None


def fetch_coingecko_ohlcv(coin_id: str, days: int = 90):
    """
    Fallback OHLCV from CoinGecko.
    CoinGecko uses daily candles only.
    """
    try:
        url = COINGECKO_BASE.format(id=coin_id)
        params = {"vs_currency": "usd", "days": days}

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        prices = data.get("prices", [])
        if not prices:
            return None

        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["price"]
        df["high"] = df["price"]
        df["low"] = df["price"]
        df["close"] = df["price"]
        df["volume"] = 0.0

        return df[["date", "open", "high", "low", "close", "volume"]]

    except Exception:
        return None


def get_ohlcv(symbol: str, interval: str, days: int = 90, coingecko_id: str = None):
    """
    Unified function:
    1. Try Binance
    2. If Binance fails → try CoinGecko
    """
    df = fetch_binance_ohlcv(symbol, interval, days)
    if df is not None:
        return df

    if coingecko_id:
        return fetch_coingecko_ohlcv(coingecko_id, days)

    return None