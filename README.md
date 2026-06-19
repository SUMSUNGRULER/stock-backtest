# Stock Backtesting: SMA Crossover Strategy

A beginner-friendly Python project that simulates a simple algorithmic trading strategy on synthetic stock price data — no real money, no brokerage account required.

Built as a portfolio project to demonstrate applied Python, financial mathematics, and data visualization.

---

## What This Project Does

The program:
1. **Generates** 500 days of fake (but realistic) stock price data using a Geometric Brownian Motion model
2. **Computes** two Simple Moving Averages (20-day and 50-day) on that price data
3. **Signals** a BUY when the short SMA crosses above the long SMA, and a SELL when it crosses below
4. **Simulates** a $10,000 portfolio trading those signals day by day
5. **Measures** performance using Total Return, Max Drawdown, and Sharpe Ratio
6. **Plots** three charts saved to the `charts/` folder

---

## The Strategy: SMA Crossover

A **Simple Moving Average (SMA)** smooths out the noise in daily price data by averaging the closing price over the last N days. Using two SMAs of different lengths creates a trend-following system:

```
Short SMA (20-day) ──── reacts quickly to recent price moves
Long  SMA (50-day) ──── reflects the broader, slower trend
```

| Event | Name | Action |
|-------|------|--------|
| Short SMA crosses **above** long SMA | "Golden Cross" | **BUY** |
| Short SMA crosses **below** long SMA | "Death Cross"  | **SELL** |

The strategy is always either fully invested or fully in cash — no partial positions.

---

## Project Structure

```
stock-backtest/
├── main.py                  ← Run this to execute the full backtest
├── requirements.txt         ← Python libraries needed
│
├── data/
│   └── generate_data.py     ← Synthetic stock price generator (GBM model)
│
├── strategy/
│   └── sma_crossover.py     ← Computes SMAs and generates buy/sell signals
│
├── backtest/
│   └── engine.py            ← Simulates trades and tracks portfolio value
│
├── metrics/
│   └── performance.py       ← Calculates Total Return, Max Drawdown, Sharpe Ratio
│
└── charts/                  ← Output charts are saved here (created on first run)
    ├── 1_price_and_signals.png
    ├── 2_portfolio_value.png
    └── 3_drawdown.png
```

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/stock-backtest.git
cd stock-backtest
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the backtest
```bash
python main.py
```

You will see a performance summary printed to the terminal and three chart images saved in the `charts/` folder.

---

## Sample Output

```
================================================
        BACKTEST PERFORMANCE SUMMARY
================================================
  Initial Capital ($)               10000.00
  Final Portfolio Value ($)         12453.78
  Strategy Total Return (%)            24.54
  Buy & Hold Total Return (%)          31.20
  Strategy Max Drawdown (%)           -11.83
  Buy & Hold Max Drawdown (%)         -17.42
  Strategy Sharpe Ratio                 0.847
  Buy & Hold Sharpe Ratio               0.763
  Number of Buys                            6
  Number of Sells                           6
  Complete Round-Trips                      6
================================================
```

### Chart 1 — Price and Signals
Shows the stock price, both SMAs, and the exact days buy (▲) and sell (▼) signals were triggered.

### Chart 2 — Portfolio Value vs Buy & Hold
The bottom-line comparison: did active trading outperform simply holding?

### Chart 3 — Drawdown
Shows how far the portfolio fell from its peak at any point — a key measure of risk.

---

## Performance Metrics Explained

| Metric | Formula | What it tells you |
|--------|---------|-------------------|
| **Total Return** | (Final − Initial) / Initial × 100 | Overall profit or loss as a percentage |
| **Max Drawdown** | Worst peak-to-trough drop | The most painful losing streak — measures downside risk |
| **Sharpe Ratio** | (Avg excess return) / (Std dev of returns) × √252 | Return per unit of risk; above 1.0 is generally good |

---

## Key Concepts I Learned

- **Geometric Brownian Motion** — a stochastic process used in quantitative finance to model asset prices; grounded in the same math as the Black-Scholes option pricing model
- **Moving Averages** — a fundamental signal-smoothing technique used across finance, engineering, and data science
- **Backtesting** — the practice of testing a trading strategy on historical data before risking real capital; subject to overfitting bias
- **Sharpe Ratio** — a Nobel Prize-winning risk-adjustment metric developed by William Sharpe
- **Drawdown analysis** — separates strategies that earn the same return but carry very different risk profiles

---

## Limitations & Honest Caveats

- **Synthetic data** — real markets have fat tails, regime changes, and gaps that a GBM model does not capture
- **No transaction costs** — real trades incur commissions and bid-ask spreads
- **No slippage** — assumes we can always buy/sell exactly at the closing price
- **Look-ahead bias is avoided** — signals are only generated from prices already observed
- **This is for learning, not financial advice**

---

## Built With

- [pandas](https://pandas.pydata.org/) — data manipulation
- [NumPy](https://numpy.org/) — numerical computing
- [Matplotlib](https://matplotlib.org/) — data visualization

---

## Author

Author: Wei Wu

