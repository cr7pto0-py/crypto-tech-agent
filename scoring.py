import numpy as np
import pandas as pd


def normalize(value, min_val, max_val):
    """Normalize any indicator into a 0–100 score."""
    if value is None or np.isnan(value):
        return 50
    return max(0, min(100, 100 * (value - min_val) / (max_val - min_val)))


def score_macd(df):
    hist = df["macd_hist"].iloc[-1]
    return normalize(hist, -0.02, 0.02)


def score_adx(df):
    adx = df["adx"].iloc[-1]
    return normalize(adx, 10, 40)


def score_ma_cross(df):
    cross = df["ma_cross"].iloc[-1]
    return normalize(cross, -5, 5)


def score_ao(df):
    ao = df["ao"].iloc[-1]
    return normalize(ao, -20, 20)


def score_rsi(df):
    rsi = df["rsi"].iloc[-1]
    return normalize(rsi, 30, 70)


def score_cci(df):
    cci = df["cci"].iloc[-1]
    return normalize(cci, -200, 200)


def score_williams_r(df):
    wr = df["williams_r"].iloc[-1]
    return normalize(wr, -100, 0)


def score_swing_index(df):
    si = df["swing_index"].iloc[-1]
    return normalize(si, -1, 1)


def compute_confidence(df):
    """
    Confidence is based on:
    - ADX trend strength
    - Data completeness
    - Indicator stability
    """
    adx = df["adx"].iloc[-1]
    stability = df["close"].pct_change().rolling(10).std().iloc[-1]

    adx_score = normalize(adx, 10, 40)
    stability_score = 100 - normalize(stability, 0, 0.05)

    return int((adx_score * 0.6) + (stability_score * 0.4))


def compute_indicator_scores(df):
    return {
        "macd": score_macd(df),
        "adx": score_adx(df),
        "ma_cross": score_ma_cross(df),
        "ao": score_ao(df),
        "rsi": score_rsi(df),
        "cci": score_cci(df),
        "williams_r": score_williams_r(df),
        "swing_index": score_swing_index(df),
        "confidence": compute_confidence(df)
    }


def blend_timeframes(scores_1d, scores_4h, scores_1h):
    """
    Blend the three timeframes using your weights:
    - 1D: 50%
    - 4H: 30%
    - 1H: 20%
    """
    weights = {"1d": 0.5, "4h": 0.3, "1h": 0.2}

    blended = {}
    for key in scores_1d.keys():
        blended[key] = (
            scores_1d[key] * weights["1d"] +
            scores_4h[key] * weights["4h"] +
            scores_1h[key] * weights["1h"]
        )

    return blended