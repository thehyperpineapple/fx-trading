"""
Example Usage of the Trading Strategy Backtesting System
=========================================================

This script demonstrates how to use the main backtesting function
with different configurations.
"""

from strategy import run_backtest

# ============================================================================
# Example 1: Basic usage without macroeconomic variables
# ============================================================================
print("=" * 70)
print("Example 1: Strategy WITHOUT Macroeconomic Variables")
print("=" * 70)

results_no_macro = run_backtest(
    ticker="EURUSD=X",              # FX pair ticker
    start_date="2024-01-01",        # Start date
    end_date="2025-01-01",          # End date
    threshold=0.00015,              # Crossover threshold
    deceleration_rate=0.0005,       # Exit deceleration rate
    use_macro=False,                # Don't use macro variables
    initial_capital=10000,          # Starting capital
    grid_search_step=0.05,         # Grid search step size
    plot_results=True               # Show plots
)

# Access results
print("\nBest Parameters:", results_no_macro['best_params'])
print("Metrics:", results_no_macro['metrics'])

# ============================================================================
# Example 2: With macroeconomic variables
# ============================================================================
print("\n" + "=" * 70)
print("Example 2: Strategy WITH Macroeconomic Variables")
print("=" * 70)

results_with_macro = run_backtest(
    ticker="EURUSD=X",
    start_date="2024-01-01",
    end_date="2025-01-01",
    threshold=0.0015,               # Different threshold
    deceleration_rate=0.005,        # Different deceleration rate
    use_macro=True,                 # Use macro variables
    initial_capital=10000,
    grid_search_step=0.05,
    plot_results=True
)

# Compare results
print("\n" + "=" * 70)
print("Comparison Summary")
print("=" * 70)
print(f"Without Macro - Sharpe: {results_no_macro['metrics']['Sharpe Ratio']:.4f}")
print(f"With Macro    - Sharpe: {results_with_macro['metrics']['Sharpe Ratio']:.4f}")

# ============================================================================
# Example 3: Custom parameters for different time period
# ============================================================================
print("\n" + "=" * 70)
print("Example 3: Different Time Period")
print("=" * 70)

results_custom = run_backtest(
    ticker="EURUSD=X",
    start_date="2023-01-01",
    end_date="2024-01-01",
    threshold=0.0002,
    deceleration_rate=0.0008,
    use_macro=False,
    initial_capital=10000,
    plot_results=False              # Don't show plots
)

print(f"Sharpe Ratio: {results_custom['metrics']['Sharpe Ratio']:.4f}")
print(f"Total Trades: {results_custom['metrics']['Total Trades']}")
