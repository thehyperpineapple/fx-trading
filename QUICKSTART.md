# Quick Start Guide

## Running the Streamlit Application

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **The app will open in your browser** at `http://localhost:8501`

## Using the Application

1. **Configure Parameters** in the sidebar:
   - Enter ticker symbol (e.g., `EURUSD=X`)
   - Select start and end dates
   - Set threshold and deceleration rate
   - Set initial capital
   - Optionally enable macroeconomic variables
   - Adjust grid search step size

2. **Click "Run Backtest"** button

3. **View Results**:
   - Optimal parameters (Alpha and Beta)
   - Performance metrics (displayed as cards)
   - Sharpe Ratio Heatmap
   - Price, Indicators & Equity Curve chart
   - Trade log table (with download option)

## Example Parameters

For quick testing, use these default values:
- **Ticker**: EURUSD=X
- **Start Date**: 2024-01-01
- **End Date**: 2025-01-01
- **Threshold**: 0.00015
- **Deceleration Rate**: 0.0005
- **Initial Capital**: $10,000
- **Use Macro**: False
- **Grid Search Step**: 0.05

## Troubleshooting

- **If data download fails**: Check your internet connection and verify the ticker symbol
- **If macro data fails**: The app will use a fallback signal (all 1s)
- **If grid search is slow**: Increase the grid search step size (e.g., 0.1 instead of 0.05)

