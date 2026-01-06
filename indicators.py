import pandas as pd
import numpy as np
import ta


def add_macd(df: pd.DataFrame):
    macd = ta.trend.MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()
    return df


def add_adx(df: pd.DataFrame):
    adx = ta.trend.ADXIndicator(
        high=df["high"], low=df["low"], close=df["close"]
    )
    df["adx"] = adx.adx()
    return df


def add_ma_cross(df: pd.DataFrame, fast=20, slow=50):
    df["ma_fast"] = df["close"].rolling(fast).mean()
    df["ma_slow"] = df["close"].rolling(slow).mean()
    df["ma_cross"] = df["ma_fast"] - df["ma_slow"]
    return df


def add_awesome_oscillator(df: pd.DataFrame):
    ao = ta.momentum.AwesomeOscillatorIndicator(
        high=df["high"], low=df["low"]
    )
    df["ao"] = ao.awesome_oscillator()
    return df


def add_rsi(df: pd.DataFrame, period=14):
    rsi = ta.momentum.RSIIndicator(close=df["close"], window=period)
    df["rsi"] = rsi.rsi()
    return df


def add_cci(df: pd.DataFrame, period=20):
    cci = ta.trend.CCIIndicator(
        high=df["high"], low=df["low"], close=df["close"], window=period
    )
    df["cci"] = cci.cci()
    return df


def add_williams_r(df: pd.DataFrame, period=14):
    wr = ta.momentum.WilliamsRIndicator(
        high=df["high"], low=df["low"], close=df["close"], lbp=period
    )
    df["williams_r"] = wr.williams_r()
    return df


def add_swing_index(df: pd.DataFrame):
    """
    Simplified Swing Index approximation.
    True Swing Index requires more data than Binance provides.
    """
    df["swing_index"] = (df["close"] - df["open"]) / (df["high"] - df["low"] + 1e-9)
    return df


def add_all_indicators(df: pd.DataFrame):
    """
    Apply all indicators in one unified function.
    """
    df = add_macd(df)
    df = add_adx(df)
    df = add_ma_cross(df)
    df = add_awesome_oscillator(df)
    df = add_rsi(df)
    df = add_cci(df)
    df = add_williams_r(df)
    df = add_swing_index(df)

    return df
