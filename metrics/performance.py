"""
metrics/performance.py
----------------------
Calculates performance statistics to evaluate how well the strategy did.

These metrics are standard in quantitative finance and show up in every
real hedge fund or algorithmic trading report:

  Total Return   — did we make money overall?
  Max Drawdown   — what was the worst losing streak? (measures risk)
  Sharpe Ratio   — how much return did we earn per unit of risk?
  Trade Count    — how often did the strategy trade?
"""

import numpy as np
import pandas as pd


def total_return(portfolio_values: pd.Series) -> float:
    """
    Percentage gain or loss from start to end.

    Formula: (final_value - initial_value) / initial_value × 100
    Example: 10000 → 12500 gives +25.0%
    """
    initial = portfolio_values.iloc[0]
    final = portfolio_values.iloc[-1]
    return (final - initial) / initial * 100


def max_drawdown(portfolio_values: pd.Series) -> float:
    """
    The largest peak-to-trough percentage drop in portfolio value.

    This measures risk: even if the strategy ended up profitable,
    a large drawdown means you had to endure painful paper losses along the way.

    Example: if the portfolio went $10k → $8k before recovering to $12k,
             the max drawdown is (8k - 10k) / 10k = -20%.
    """
    # Running maximum up to each day (the "peak" seen so far).
    rolling_peak = portfolio_values.cummax()

    # How far below the peak are we each day?
    drawdown = (portfolio_values - rolling_peak) / rolling_peak * 100

    # The worst (most negative) drawdown over the entire period.
    return drawdown.min()


def sharpe_ratio(portfolio_values: pd.Series, risk_free_rate: float = 0.04) -> float:
    """
    Risk-adjusted return: how much excess return per unit of volatility?

    A Sharpe ratio above 1.0 is generally considered decent.
    Above 2.0 is very good. Below 0 means you'd have been better off in
    a risk-free investment (like a savings account).

    Parameters
    ----------
    portfolio_values : daily portfolio value series
    risk_free_rate   : annualised risk-free rate (default 4%, typical for T-bills)
    """
    # Daily percentage returns
    daily_returns = portfolio_values.pct_change().dropna()

    # Subtract the daily equivalent of the risk-free rate
    daily_rf = risk_free_rate / 252
    excess_returns = daily_returns - daily_rf

    if excess_returns.std() == 0:
        return 0.0

    # Annualise: multiply by √252 to convert daily Sharpe to yearly Sharpe
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)


def count_trades(trade_col: pd.Series) -> dict:
    """
    Count how many buy and sell events occurred.
    """
    buys = (trade_col == "BUY").sum()
    sells = (trade_col == "SELL").sum()
    return {"buys": int(buys), "sells": int(sells), "total_roundtrips": int(min(buys, sells))}


def summarise(df: pd.DataFrame, initial_capital: float = 10_000.0) -> dict:
    """
    Compute and return all metrics in one dictionary.

    Parameters
    ----------
    df              : DataFrame output from run_backtest()
    initial_capital : Starting cash (used for display purposes)

    Returns
    -------
    Dictionary of metric names → values, ready to print or log.
    """
    strategy_values = df["Portfolio_Value"]
    buyhold_values = df["BuyHold_Value"]
    trades = count_trades(df["Trade"])

    return {
        "Initial Capital ($)":        round(initial_capital, 2),
        "Final Portfolio Value ($)":   round(strategy_values.iloc[-1], 2),
        "Strategy Total Return (%)":   round(total_return(strategy_values), 2),
        "Buy & Hold Total Return (%)": round(total_return(buyhold_values), 2),
        "Strategy Max Drawdown (%)":   round(max_drawdown(strategy_values), 2),
        "Buy & Hold Max Drawdown (%)": round(max_drawdown(buyhold_values), 2),
        "Strategy Sharpe Ratio":       round(sharpe_ratio(strategy_values), 3),
        "Buy & Hold Sharpe Ratio":     round(sharpe_ratio(buyhold_values), 3),
        "Number of Buys":              trades["buys"],
        "Number of Sells":             trades["sells"],
        "Complete Round-Trips":        trades["total_roundtrips"],
    }
