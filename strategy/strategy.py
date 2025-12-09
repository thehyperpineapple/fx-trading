"""
Strategy Execution Module
=========================
Functions for running the trading strategy.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple

from strategy.metrics import calculate_metrics


def run_strategy(
    data: pd.DataFrame,
    alpha: float,
    beta: float,
    threshold: float = 0.001,
    decel_rate: float = 0.0005,
    initial_capital: float = 10000,
    macro_df: Optional[pd.DataFrame] = None
) -> Tuple[Dict[str, float], pd.DataFrame, pd.DataFrame]:
    """
    Runs the trading strategy with exponential smoothing indicators.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Price data with 'Close' column
    alpha : float
        Slow exponential smoothing parameter
    beta : float
        Fast exponential smoothing parameter
    threshold : float
        Crossover threshold for entry signals
    decel_rate : float
        Deceleration rate for exit signals
    initial_capital : float
        Starting capital
    macro_df : pd.DataFrame, optional
        Macroeconomic signals DataFrame with 'Macro_Signal' column
    
    Returns:
    --------
    Tuple[Dict, pd.DataFrame, pd.DataFrame]
        (metrics, strategy_df, trades_df)
    """
    df = data.copy()

    # Calculate indicators
    df['es_slow'] = df['Close'].ewm(alpha=alpha, adjust=False).mean()
    df['es_fast'] = df['Close'].ewm(alpha=beta, adjust=False).mean()
    df['diff'] = df['es_fast'] - df['es_slow']
    df['velocity'] = df['es_fast'].diff()
    df['acceleration'] = df['velocity'].diff()

    # Join macro data if provided
    if macro_df is not None:
        df = df.join(macro_df[['Macro_Signal']], how='left').ffill()
    else:
        df['Macro_Signal'] = 1  # Neutral signal (no macro filtering)

    # Initialize tracking variables
    position = 0
    entry_price = 0.0
    equity = [initial_capital] * len(df)
    trade_log = []
    trade_dates = []
    trade_types = []
    trade_prices = []

    # Main trading loop
    for i in range(2, len(df)):
        curr_price = df['Close'].iloc[i]
        prev_price = df['Close'].iloc[i-1]
        date = df.index[i]

        curr_diff = df['diff'].iloc[i]
        prev_diff = df['diff'].iloc[i-1]
        curr_accel = df['acceleration'].iloc[i]
        macro_signal = df['Macro_Signal'].iloc[i]

        # Mark-to-Market
        if position == 1:
            pct_change = (curr_price - prev_price) / prev_price
            equity[i] = equity[i-1] * (1 + pct_change)
        elif position == -1:
            pct_change = (prev_price - curr_price) / prev_price
            equity[i] = equity[i-1] * (1 + pct_change)
        else:
            equity[i] = equity[i-1]

        # Exit (Deceleration)
        if position == 1 and curr_accel < -decel_rate:
            trade_log.append(curr_price - entry_price)
            position = 0
            trade_dates.append(date)
            trade_types.append('Exit Long')
            trade_prices.append(curr_price)
        elif position == -1 and curr_accel > decel_rate:
            trade_log.append(entry_price - curr_price)
            position = 0
            trade_dates.append(date)
            trade_types.append('Exit Short')
            trade_prices.append(curr_price)

        # Entry
        # Long entry: crossover up + macro confirmation (if using macro)
        if prev_diff < 0 and curr_diff > threshold:
            if macro_df is not None:
                # Require macro confirmation
                if macro_signal > 0:
                    if position == -1:
                        trade_log.append(entry_price - curr_price)
                    position = 1
                    entry_price = curr_price
                    trade_dates.append(date)
                    trade_types.append('Buy')
                    trade_prices.append(curr_price)
            else:
                # No macro filtering
                if position == -1:
                    trade_log.append(entry_price - curr_price)
                position = 1
                entry_price = curr_price
                trade_dates.append(date)
                trade_types.append('Buy')
                trade_prices.append(curr_price)

        # Short entry: crossover down + macro confirmation (if using macro)
        elif prev_diff > 0 and curr_diff < -threshold:
            if macro_df is not None:
                # Require macro confirmation
                if macro_signal < 0:
                    if position == 1:
                        trade_log.append(curr_price - entry_price)
                    position = -1
                    entry_price = curr_price
                    trade_dates.append(date)
                    trade_types.append('Sell')
                    trade_prices.append(curr_price)
            else:
                # No macro filtering
                if position == 1:
                    trade_log.append(curr_price - entry_price)
                position = -1
                entry_price = curr_price
                trade_dates.append(date)
                trade_types.append('Sell')
                trade_prices.append(curr_price)

    df['Equity'] = equity

    # Safety check for empty trade_log
    if not trade_log:
        trade_log = [0]

    metrics = calculate_metrics(pd.Series(df['Equity'], index=df.index), trade_log)
    trades_df = pd.DataFrame({
        'Date': trade_dates,
        'Type': trade_types,
        'Price': trade_prices
    })

    return metrics, df, trades_df

