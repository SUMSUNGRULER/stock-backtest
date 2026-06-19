"""
sma_crossover.py
----------------
Implements the Simple Moving Average (SMA) Crossover strategy.

A Simple Moving Average smooths out daily price noise by averaging the
closing price over the last N days. Two SMAs with different window lengths
are used to detect trend changes:

  - Short SMA (e.g. 20 days): reacts quickly to recent price moves
  - Long  SMA (e.g. 50 days): reflects the broader, slower trend

Trading signals:
  BUY  (+1) when short SMA crosses ABOVE long SMA  → uptrend starting
  SELL (-1) when short SMA crosses BELOW long SMA  → downtrend starting
  HOLD  (0) on all other days
"""

import pandas as pd


def compute_signals(
    df: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.DataFrame:
    """
    Add SMA columns and a daily signal column to the price DataFrame.

    Parameters
    ----------
    df            : DataFrame with a 'Close' column (from generate_data.py).
    short_window  : Number of days for the fast-moving average.
    long_window   : Number of days for the slow-moving average.

    Returns
    -------
    The same DataFrame with three new columns added:
        'SMA_short' : short moving average
        'SMA_long'  : long moving average
        'Signal'    : +1 (buy), -1 (sell), or 0 (hold)
    """

    df = df.copy()  # Never modify the original data — work on a copy.

    # rolling(n).mean() looks at the last n rows and computes the average.
    # The first (n-1) rows will be NaN because there aren't enough prior days.
    df["SMA_short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_long"] = df["Close"].rolling(window=long_window).mean()

    # Determine the "regime" each day: is the short SMA above the long SMA?
    # True (1) means short > long → bullish; False (0) means short < long → bearish.
    df["SMA_short_above"] = (df["SMA_short"] > df["SMA_long"]).astype(int)

    # A crossover happens when the regime CHANGES from one day to the next.
    # diff() subtracts the previous row's value from the current row's value.
    #   +1 means it flipped from 0→1 (short crossed above) → BUY signal
    #   -1 means it flipped from 1→0 (short crossed below) → SELL signal
    #    0 means no change → hold
    df["Signal"] = df["SMA_short_above"].diff().fillna(0).astype(int)

    return df
