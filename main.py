"""
main.py
-------
Entry point for the stock backtesting project.

Run this file to:
  1. Generate synthetic stock price data
  2. Compute SMA crossover signals
  3. Simulate the strategy with a $10,000 starting portfolio
  4. Print performance metrics
  5. Save three charts to the charts/ folder
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from data.generate_data import generate_stock_prices
from strategy.sma_crossover import compute_signals
from backtest.engine import run_backtest
from metrics.performance import summarise

# ── Configuration ─────────────────────────────────────────────────────────────
INITIAL_CAPITAL = 10_000   # Starting cash in dollars
SHORT_WINDOW    = 20       # Days for the fast (short) moving average
LONG_WINDOW     = 50       # Days for the slow (long)  moving average
N_DAYS          = 500      # Trading days to simulate (~2 years)
CHARTS_DIR      = "charts"
# ──────────────────────────────────────────────────────────────────────────────


def print_metrics(metrics: dict) -> None:
    """Print the performance summary in a readable table format."""
    print("\n" + "=" * 48)
    print("        BACKTEST PERFORMANCE SUMMARY")
    print("=" * 48)
    for name, value in metrics.items():
        # Right-align the value in a fixed-width column
        print(f"  {name:<34} {value:>9}")
    print("=" * 48 + "\n")


def plot_price_and_signals(df, save_path: str) -> None:
    """
    Chart 1: Stock price with the two SMAs overlaid, and buy/sell markers.

    This is the most important chart — it shows you exactly when the strategy
    decided to buy or sell, and whether those decisions made sense visually.
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df.index, df["Close"],     label="Price",     color="#4C72B0", linewidth=1.2, alpha=0.8)
    ax.plot(df.index, df["SMA_short"], label=f"SMA {SHORT_WINDOW}d", color="#DD8452", linewidth=1.5)
    ax.plot(df.index, df["SMA_long"],  label=f"SMA {LONG_WINDOW}d",  color="#55A868", linewidth=1.5)

    # Mark BUY signals with upward green triangles
    buys = df[df["Trade"] == "BUY"]
    ax.scatter(buys.index, buys["Close"], marker="^", color="green",
               s=120, zorder=5, label="BUY signal")

    # Mark SELL signals with downward red triangles
    sells = df[df["Trade"] == "SELL"]
    ax.scatter(sells.index, sells["Close"], marker="v", color="red",
               s=120, zorder=5, label="SELL signal")

    ax.set_title("Stock Price with SMA Crossover Signals", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Saved: {save_path}")


def plot_portfolio_value(df, save_path: str) -> None:
    """
    Chart 2: Strategy portfolio value vs buy-and-hold over time.

    This is the bottom-line chart: did our strategy beat doing nothing?
    """
    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(df.index, df["Portfolio_Value"], label="SMA Strategy",  color="#4C72B0", linewidth=2)
    ax.plot(df.index, df["BuyHold_Value"],   label="Buy & Hold",    color="#DD8452", linewidth=2, linestyle="--")

    ax.set_title("Portfolio Value: Strategy vs Buy & Hold", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Saved: {save_path}")


def plot_drawdown(df, save_path: str) -> None:
    """
    Chart 3: Drawdown over time for the strategy and buy-and-hold.

    Drawdown shows how far the portfolio has fallen from its previous peak.
    Deep drawdowns are psychologically hard to endure — this chart makes
    the risk visible.
    """
    def compute_drawdown_series(series):
        rolling_peak = series.cummax()
        return (series - rolling_peak) / rolling_peak * 100

    strategy_dd = compute_drawdown_series(df["Portfolio_Value"])
    buyhold_dd  = compute_drawdown_series(df["BuyHold_Value"])

    fig, ax = plt.subplots(figsize=(14, 4))

    ax.fill_between(df.index, strategy_dd, 0, alpha=0.4, color="#4C72B0", label="SMA Strategy")
    ax.fill_between(df.index, buyhold_dd,  0, alpha=0.3, color="#DD8452", label="Buy & Hold")
    ax.plot(df.index, strategy_dd, color="#4C72B0", linewidth=1)
    ax.plot(df.index, buyhold_dd,  color="#DD8452", linewidth=1, linestyle="--")

    ax.set_title("Drawdown Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Saved: {save_path}")


def main():
    print("Running SMA Crossover Backtest...")
    print(f"  Parameters: short_window={SHORT_WINDOW}, long_window={LONG_WINDOW}, "
          f"capital=${INITIAL_CAPITAL:,}, days={N_DAYS}\n")

    # Step 1: Generate synthetic price data
    print("Step 1: Generating synthetic stock prices...")
    price_df = generate_stock_prices(n_days=N_DAYS)

    # Step 2: Compute SMA signals
    print("Step 2: Computing SMA crossover signals...")
    signal_df = compute_signals(price_df, short_window=SHORT_WINDOW, long_window=LONG_WINDOW)

    # Step 3: Run the backtest simulation
    print("Step 3: Running backtest simulation...")
    result_df = run_backtest(signal_df, initial_capital=INITIAL_CAPITAL)

    # Step 4: Calculate and print performance metrics
    print("Step 4: Calculating performance metrics...")
    metrics = summarise(result_df, initial_capital=INITIAL_CAPITAL)
    print_metrics(metrics)

    # Step 5: Save charts
    print("Step 5: Generating charts...")
    os.makedirs(CHARTS_DIR, exist_ok=True)
    plot_price_and_signals(result_df, os.path.join(CHARTS_DIR, "1_price_and_signals.png"))
    plot_portfolio_value(result_df,   os.path.join(CHARTS_DIR, "2_portfolio_value.png"))
    plot_drawdown(result_df,          os.path.join(CHARTS_DIR, "3_drawdown.png"))

    print("\nDone! Check the charts/ folder for the generated plots.")


if __name__ == "__main__":
    main()
