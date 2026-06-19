"""
generate_data.py
----------------
Creates fake (synthetic) stock price data so we don't need a real API or
real money. We use a "Geometric Brownian Motion" (GBM) model — the same
mathematical model taught in quantitative finance courses to describe how
stock prices move randomly over time.

GBM formula each day:
    price_today = price_yesterday * exp(daily_drift + daily_volatility * random_shock)

Where:
    - daily_drift   = small upward trend (like a stock that grows ~10% per year)
    - daily_volatility = how much the price swings day to day (~20% per year)
    - random_shock  = a random number drawn from a normal distribution
"""

import numpy as np
import pandas as pd


def generate_stock_prices(
    start_price: float = 100.0,
    n_days: int = 500,
    annual_drift: float = 0.10,
    annual_volatility: float = 0.20,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a synthetic stock price history.

    Parameters
    ----------
    start_price       : The price on day 1 (in dollars).
    n_days            : How many trading days to simulate.
    annual_drift      : Expected yearly return (0.10 = 10% per year).
    annual_volatility : Yearly price swing (0.20 = 20% per year).
    seed              : Random seed so results are reproducible.

    Returns
    -------
    A pandas DataFrame with columns: ['Date', 'Close']
    """

    # Fix the random seed so the same "random" data is generated every run.
    # This makes results reproducible — important for debugging and demos.
    np.random.seed(seed)

    # Convert annual numbers to daily numbers.
    # There are ~252 trading days in a year.
    trading_days_per_year = 252
    daily_drift = annual_drift / trading_days_per_year
    daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

    # Generate one random shock per day from a standard normal distribution.
    random_shocks = np.random.normal(loc=0, scale=1, size=n_days)

    # Calculate the daily percentage change using the GBM formula.
    # np.exp converts from log-space to regular price space.
    daily_returns = np.exp(daily_drift - 0.5 * daily_volatility**2 + daily_volatility * random_shocks)

    # Build the price series by multiplying each day's return cumulatively.
    # np.cumprod gives the running product: [r1, r1*r2, r1*r2*r3, ...]
    prices = start_price * np.cumprod(daily_returns)

    # Create a date index of business days (Mon–Fri), skipping weekends.
    dates = pd.bdate_range(start="2022-01-03", periods=n_days)

    # Package everything into a DataFrame (like a table / spreadsheet).
    df = pd.DataFrame({"Date": dates, "Close": prices})
    df.set_index("Date", inplace=True)

    return df
