# IEOR4571 EUR/USD Trading

Design and test a trading algorithm using both traditional time-series techniques and modern machine learning methods for FX Trading (EUR/USD).

## Features

- **Exponential Smoothing Strategy**: Uses fast and slow exponential smoothing indicators
- **Macroeconomic Integration**: Optional filtering based on GDP and Current Account data
- **Parameter Optimization**: Automatic grid search for optimal alpha/beta parameters
- **Comprehensive Metrics**: Annual return, Sharpe ratio, max drawdown, hit rate, and more
- **Interactive Web Interface**: Streamlit-based UI for easy parameter configuration
- **Visualizations**: Heatmaps and trade charts

## Installation

1. **Install Python 3.11** (if not already installed)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Streamlit Web Application (Recommended)

Run the interactive web application:

```bash
streamlit run app.py
```

The application will open in your default web browser. You can:
- Input all strategy parameters in the sidebar
- View performance metrics
- See visualizations (heatmap and trade charts)
- Download trade logs

### Option 2: Python Script

Run the main script:

```bash
python main.py
```

### Option 3: Import as Package

Use the strategy package in your own code:

```python
from strategy import run_backtest

results = run_backtest(
    ticker="EURUSD=X",
    start_date="2024-01-01",
    end_date="2025-01-01",
    threshold=0.00015,
    deceleration_rate=0.0005,
    use_macro=False,
    initial_capital=10000
)

print(results['metrics'])
```

## Parameters

- **ticker**: Ticker symbol (e.g., "EURUSD=X" for FX pairs)
- **start_date**: Start date in "YYYY-MM-DD" format
- **end_date**: End date in "YYYY-MM-DD" format
- **threshold**: Crossover threshold for entry signals (default: 0.00015)
- **deceleration_rate**: Deceleration rate for exit signals (default: 0.0005)
- **use_macro**: Whether to use macroeconomic variables (default: False)
- **initial_capital**: Starting capital (default: 10000)
- **grid_search_step**: Step size for parameter optimization (default: 0.05)

## Project Structure

```
Project/
├── app.py                      # Streamlit web application
├── main.py                     # Main script entry point
├── example_usage.py            # Example usage script
├── requirements.txt            # Python dependencies
├── strategy/                   # Strategy package
│   ├── __init__.py            # Package initialization
│   ├── data.py                # Data fetching functions
│   ├── metrics.py             # Performance metrics calculation
│   ├── strategy.py            # Strategy execution
│   ├── optimization.py        # Parameter optimization
│   └── visualization.py       # Plotting functions
└── README.md                   # This file
```

## Performance Metrics

The system calculates the following metrics:

- **Annual Return**: Annualized return percentage
- **Annual Volatility**: Annualized volatility percentage
- **Sharpe Ratio**: Risk-adjusted return metric
- **Max Drawdown**: Maximum peak-to-trough decline
- **Hit Rate**: Percentage of winning trades
- **Total Trades**: Number of trades executed
- **Avg Win**: Average profit per winning trade
- **Avg Loss**: Average loss per losing trade
- **Win/Loss Ratio**: Ratio of average win to average loss

## Notes

- Using macroeconomic variables requires fetching data from FRED and may take longer
- Smaller grid search step sizes provide more thorough optimization but take longer to compute
- The strategy uses exponential smoothing with crossover signals for entries and deceleration for exits

## Requirements

See `requirements.txt` for the complete list of dependencies. Key packages include:
- pandas
- numpy
- yfinance
- pandas-datareader
- matplotlib
- seaborn
- streamlit