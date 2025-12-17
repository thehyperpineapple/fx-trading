# IEOR4571 EUR/USD Trading

A comprehensive FX trading system that combines traditional time-series techniques with modern machine learning methods for EUR/USD trading. The project includes both rule-based strategies (exponential smoothing with macroeconomic filters) and advanced ML approaches (ensemble models, LSTM, and regime-aware models).

## Features

### Traditional Time-Series Approach
- **Exponential Smoothing Strategy**: Uses fast and slow exponential smoothing indicators
- **Macroeconomic Integration**: Optional filtering based on GDP and Current Account data
- **Parameter Optimization**: Automatic grid search for optimal alpha/beta parameters
- **Interactive Web Interface**: Streamlit-based UI for easy parameter configuration
- **Visualizations**: Heatmaps and trade charts

### Machine Learning Approach
- **Multiple Model Architectures**: Logistic Regression, Naive Bayes, Random Forest, Gradient Boosting, SVM, XGBoost, LightGBM, CatBoost, HistGBM, and LSTM
- **Ensemble Methods**: Soft-voting and stacking ensembles for improved predictions
- **Model Calibration**: Probability calibration using Platt scaling for better probability estimates
- **Regime-Aware Features**: Hidden Markov Model (HMM) for volatility regime detection
- **Advanced Feature Engineering**: Technical indicators, lagged OHLC features, and sequence-based features for LSTM
- **Comprehensive Evaluation**: Trading performance metrics including Sharpe ratio, hit rate, and total returns

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

## Machine Learning Approach

The project includes two comprehensive machine learning notebooks for EUR/USD trading:

### Notebooks

1. **`fx_eurusd_multi_model_regime_lstm.ipynb`**: Research-grade pipeline with:
   - Multiple ML models (Logistic, Naive Bayes, Random Forest, Gradient Boosting, SVM, XGBoost, LightGBM, CatBoost, HistGBM)
   - Calibrated versions of all models for better probability estimates
   - Ensemble methods (soft-voting and stacking)
   - LSTM sequence model for temporal patterns
   - HMM-based volatility regime detection
   - Comprehensive feature engineering (~20 technical indicators + lagged OHLC)
   - Training period: 2021-2024, Test period: 2025

2. **`fx_eurusd_assignment_ohlc_baseline.ipynb`**: Assignment-compliant baseline with:
   - Minimal OHLC-only features
   - Lookback period optimization (n = 3, 4, 5, 6, 7 days)
   - XGBoost + LightGBM ensemble
   - Training period: 2015-2024, Test period: 2025

See `notebooks/README.md` for detailed comparison of both approaches.

### Model Performance Metrics

The following table shows test set performance metrics for models trained on 2021-2024 data and evaluated on 2025 data. Models are ranked by Sharpe ratio:

| Model | AUC | Brier Score | Precision | Recall | Trades | Hit Rate | Mean Return | Sharpe Ratio | Total Return |
|-------|-----|-------------|-----------|--------|--------|----------|-------------|--------------|--------------|
| Logit | 0.602 | 0.423 | 0.251 | 0.983 | 200 | 0.260 | 0.00120 | **7.82** | 0.270 |
| Naive Bayes | 0.731 | 0.285 | 0.419 | 0.534 | 71 | 0.423 | 0.00201 | **5.87** | 0.153 |
| Ensemble Stacking | 0.559 | 0.257 | 0.289 | 0.483 | 53 | 0.491 | 0.00235 | **5.45** | 0.132 |
| Random Forest | 0.631 | 0.234 | 0.330 | 0.517 | 55 | 0.364 | 0.00172 | **4.64** | 0.099 |
| LSTM Sequence | 0.675 | 0.218 | 0.363 | 0.569 | 55 | 0.345 | 0.00163 | **4.50** | 0.093 |
| Random Forest (Cal) | 0.701 | 0.204 | 0.377 | 0.397 | 30 | 0.233 | 0.00107 | **2.58** | 0.032 |
| XGBoost | 0.602 | 0.216 | 0.294 | 0.172 | 23 | 0.261 | 0.00120 | **2.41** | 0.028 |
| CatBoost | 0.541 | 0.227 | 0.357 | 0.172 | 13 | 0.308 | 0.00144 | **1.99** | 0.019 |
| Gradient Boosting | 0.591 | 0.203 | 0.333 | 0.086 | 6 | 0.333 | 0.00157 | **1.41** | 0.009 |
| LightGBM | 0.648 | 0.242 | 0.222 | 0.034 | 7 | 0.286 | 0.00133 | **1.39** | 0.009 |
| Ensemble Soft Voting | 0.707 | 0.179 | 0.333 | 0.034 | 1 | 1.000 | 0.00490 | **1.04** | 0.005 |
| HistGBM | 0.603 | 0.207 | 0.333 | 0.086 | 5 | 0.200 | 0.00090 | **0.95** | 0.004 |

**Key Observations:**
- **Logit** achieves the highest Sharpe ratio (7.82) with high recall (98.3%) but lower precision (25.1%), resulting in many trades (200)
- **Naive Bayes** provides the best balance with high AUC (0.731), good hit rate (42.3%), and strong Sharpe (5.87)
- **LSTM** shows competitive performance (Sharpe 4.50) with good precision-recall balance
- **Ensemble Stacking** demonstrates strong hit rate (49.1%) and solid Sharpe (5.45) with fewer trades
- Calibrated models generally show improved probability estimates (lower Brier scores) but may trade less frequently

**Trading Parameters:**
- Profit target: 0.5% (Δ = 0.005)
- Trading threshold: 60% probability
- Transaction cost: 1 pip (0.0001)

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
├── strategy/                   # Strategy package (traditional approach)
│   ├── __init__.py            # Package initialization
│   ├── data.py                # Data fetching functions
│   ├── metrics.py             # Performance metrics calculation
│   ├── strategy.py            # Strategy execution
│   ├── optimization.py        # Parameter optimization
│   └── visualization.py       # Plotting functions
├── notebooks/                  # Machine learning notebooks
│   ├── fx_eurusd_multi_model_regime_lstm.ipynb  # Research-grade ML pipeline
│   ├── fx_eurusd_assignment_ohlc_baseline.ipynb # Assignment-compliant baseline
│   ├── macroeconomic_variables.ipynb            # Macro variable analysis
│   └── README.md              # Notebook comparison guide
├── metrics/                    # Model performance metrics
│   └── fx_eurusd_multi_model_regime_lstm_metrics.ipynb.csv
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

### Traditional Approach
- Using macroeconomic variables requires fetching data from FRED and may take longer
- Smaller grid search step sizes provide more thorough optimization but take longer to compute
- The strategy uses exponential smoothing with crossover signals for entries and deceleration for exits

### Machine Learning Approach
- ML notebooks require additional dependencies: `xgboost`, `lightgbm`, `catboost`, `tensorflow`, `hmmlearn`, `scikit-learn`
- Training the full model suite can take significant time (especially LSTM and ensemble methods)
- Models are trained on 2021-2024 data and tested on 2025 data to ensure realistic out-of-sample evaluation
- Probability calibration improves trading performance by providing more reliable probability estimates

## Requirements

See `requirements.txt` for the complete list of dependencies. Key packages include:

**Traditional Approach:**
- pandas
- numpy
- yfinance
- pandas-datareader
- matplotlib
- seaborn
- streamlit

**Machine Learning Approach:**
- xgboost
- lightgbm
- catboost
- tensorflow
- hmmlearn
- scikit-learn