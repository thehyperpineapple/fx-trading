"""
Trading Strategy Backtesting System
====================================
Main entry point for the trading strategy backtesting system.

This module provides a simple interface to run backtests.
All core functionality is organized in the 'strategy' package.

Usage:
    from main import run_backtest
    
    results = run_backtest(
        ticker="EURUSD=X",
        start_date="2024-01-01",
        end_date="2025-01-01",
        threshold=0.00015,
        deceleration_rate=0.0005,
        use_macro=True,
        initial_capital=10000
    )
    
    print(results['metrics'])
"""

from strategy import run_backtest


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example 1: Without macroeconomic variables
    # print("=" * 60)
    print("Example 1: Strategy WITHOUT Macroeconomic Variables")
    # print("=" * 60)
    results_no_macro = run_backtest(
        ticker="EURUSD=X",
        start_date="2024-01-01",
        end_date="2025-01-01",
        threshold=0.00015,
        deceleration_rate=0.0005,
        use_macro=False,
        initial_capital=10000,
        plot_results=False
    )

    # print("\n" + "=" * 60)
    print("Example 2: Strategy WITH Macroeconomic Variables")
    # print("=" * 60)
    results_with_macro = run_backtest(
        ticker="EURUSD=X",
        start_date="2024-01-01",
        end_date="2025-01-01",
        threshold=0.0015,
        deceleration_rate=0.005,
        use_macro=True,
        initial_capital=10000,
        plot_results=False
    )
