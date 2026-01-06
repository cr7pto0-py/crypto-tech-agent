import requests
import pandas as pd

from data_sources import get_ohlcv
from indicators import add_all_indicators
from scoring import compute_indicator_scores, blend_timeframes


COINGECKO_TOP20_URL = "https://api.coingecko.com/api/v3/coins/markets"


def get_top20_symbols(vs_currency="usd"):
    """
    Fetch top 20 cryptocurrencies by market cap from CoinGecko.
    Returns a list of dicts: {symbol, id, name}
    """
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }

    r = requests.get(COINGECKO_TOP20_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    return [
        {
            "symbol": item["symbol"].upper(),
            "id": item["id"],
            "name": item["name"]
        }
        for item in data
    ]


def process_single_asset(symbol, coingecko_id):
    """
    Fetch OHLCV for 1D, 4H, 1H.
    Apply indicators.
    Compute scores.
    Blend timeframes.
    """
    timeframes = {
        "1d": "1d",
        "4h": "4h",
        "1h": "1h"
    }

    dfs = {}
    scores = {}

    # Fetch and process each timeframe
    for tf, interval in timeframes.items():
        df = get_ohlcv(symbol, interval, days=90, coingecko_id=coingecko_id)
        if df is None or len(df) < 50:
            return None  # skip asset if data is insufficient

        df = add_all_indicators(df)
        dfs[tf] = df
        scores[tf] = compute_indicator_scores(df)

    # Blend timeframes
    blended = blend_timeframes(scores["1d"], scores["4h"], scores["1h"])

    # Compute overall rating (average of all indicators)
    indicator_keys = [
        "macd", "adx", "ma_cross", "ao",
        "rsi", "cci", "williams_r", "swing_index"
    ]
    overall_rating = sum(blended[k] for k in indicator_keys) / len(indicator_keys)

    return {
        "symbol": symbol,
        "coingecko_id": coingecko_id,
        "scores_1d": scores["1d"],
        "scores_4h": scores["4h"],
        "scores_1h": scores["1h"],
        "blended": blended,
        "overall_rating": overall_rating,
        "confidence": blended["confidence"]
    }


def run_agent(vs_currency="usd"):
    """
    Main function:
    - Fetch top 20 coins
    - Process each one
    - Return a clean DataFrame
    """
    assets = get_top20_symbols(vs_currency)
    results = []

    for asset in assets:
        result = process_single_asset(asset["symbol"], asset["id"])
        if result:
            results.append(result)

    # Convert to DataFrame for dashboard + Power BI
    rows = []
    for r in results:
        row = {
            "symbol": r["symbol"],
            "overall_rating": r["overall_rating"],
            "confidence": r["confidence"],
        }
        # Add blended indicator scores
        for k, v in r["blended"].items():
            row[f"{k}_score"] = v
        rows.append(row)

    return pd.DataFrame(rows)