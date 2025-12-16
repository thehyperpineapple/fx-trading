# FX Notebooks Overview

## Notebooks
- `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb` (research-grade, regime-aware, stacked ensemble + LSTM).
- `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb` (assignment-compliant OHLC-only baseline with lookback sweep).

## Approach comparison
- **Objective & scope**
  - `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb`: End-to-end EUR/USD research pipeline (2021–2025) with multiple learners, calibration, ensembles, and deep learning.
  - `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb`: Minimal implementation to satisfy assignment specs and quickly test OHLC lookbacks.
- **Data window & split**
  - `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb`: Downloads 2021-01-01 to 2025-11-30; trains to 2024-12-31 and tests from 2025-01-01 forward.
  - `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb`: Downloads 2015-01-01 to 2025-11-27; train/test split at 2024-12-31.
- **Features**
  - `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb`: 3-day OHLC lags, returns/ranges, ~20 technical indicators, HMM volatility regimes (lagged), and sequence windows for the LSTM.
  - `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb`: Only lagged OHLC plus simple derived ranges/returns/shadows, with SMA/volatility when lookback ≥3; no regimes or broad technical set.
- **Models**
  - `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb`: Logistic, Naive Bayes, Random Forest, Gradient Boosting, SVM, HistGBM, XGBoost, LightGBM, CatBoost, calibrated versions, soft-voting + stacking ensemble, and a Keras LSTM.
  - `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb`: Standardized XGBoost and LightGBM; simple average ensemble over the two.
- **Evaluation & trading logic**
  - `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb`: Probability threshold 60%, profit target 0.5%, cost penalty (1 pip), daily equity curve with non-trade days, Sharpe on daily returns, and position sizing via calibrated probabilities.
  - `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb`: Probability threshold 60%, profit target 0.5%; counts trades/wins/losses, return, Sharpe, drawdown, profit factor, and computes rolling 30-day Sharpe—no transaction cost adjustment.
- **Use cases**
  - `fx_eurusd_multi_model_regime_lstm.ipynb.ipynb`: Deeper research, model comparison, and production-style evaluation with regime awareness and calibration.
  - `fx_eurusd_assignment_ohlc_baseline.ipynb.ipynb`: Fast, spec-compliant baseline for comparing lookback horizons (n = 3–7) with a lightweight ensemble.


