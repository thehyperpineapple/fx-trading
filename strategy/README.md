# Strategy Package Structure

This package contains the modular components of the trading strategy backtesting system.

## Module Organization

- **`data.py`**: Data fetching functions
  - `get_price_data()`: Downloads price data from yfinance
  - `get_macro_data()`: Fetches macroeconomic data from FRED

- **`metrics.py`**: Performance metrics calculation
  - `calculate_metrics()`: Computes all performance metrics

- **`strategy.py`**: Strategy execution
  - `run_strategy()`: Runs the trading strategy with given parameters

- **`optimization.py`**: Parameter optimization
  - `perform_grid_search()`: Finds optimal alpha/beta parameters

- **`visualization.py`**: Plotting functions
  - `plot_heatmap()`: Plots Sharpe ratio heatmap
  - `plot_trades()`: Plots price, indicators, trades, and equity curve

- **`__init__.py`**: Package initialization
  - `run_backtest()`: Main user interface function
  - Exports all public functions

## Usage

Import the main function:

```python
from strategy import run_backtest

results = run_backtest(
    ticker="EURUSD=X",
    start_date="2024-01-01",
    end_date="2025-01-01",
    threshold=0.00015,
    deceleration_rate=0.0005,
    use_macro=False
)
```

Or import individual modules:

```python
from strategy.data import get_price_data
from strategy.strategy import run_strategy
from strategy.metrics import calculate_metrics
```

