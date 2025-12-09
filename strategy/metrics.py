# Metrics Calculation Module
import pandas as pd
import numpy as np
from typing import Dict


def calculate_metrics(equity_curve: pd.Series, trade_log: list) -> Dict[str, float]:
    """
    Computes performance metrics including Avg Win/Loss Ratio.
    
    Parameters:
    -----------
    equity_curve : pd.Series
        Account balance over time
    trade_log : list
        List of PnL values for each trade
    
    Returns:
    --------
    Dict[str, float]
        Dictionary of performance metrics
    """
    # Ensure trade_log is a list
    if isinstance(trade_log, pd.DataFrame):
        if 'pnl' in trade_log.columns:
            trades = trade_log['pnl'].tolist()
        else:
            try:
                trades = (trade_log['Exit_Price'] - trade_log['Entry_Price']).tolist()
            except KeyError:
                trades = []
    else:
        trades = list(trade_log)

    # Calculate returns
    daily_returns = equity_curve.pct_change().dropna()
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    days = (equity_curve.index[-1] - equity_curve.index[0]).days
    annual_return = ((1 + total_return) ** (365.0 / max(1, days))) - 1
    annual_volatility = daily_returns.std() * np.sqrt(252)

    # Sharpe Ratio
    if annual_volatility == 0:
        sharpe_ratio = 0
    else:
        sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252)

    # Drawdown
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # Win/Loss Analysis
    if len(trades) > 0:
        winners = [t for t in trades if t > 0]
        losers = [t for t in trades if t < 0]

        hit_rate = len(winners) / len(trades)
        avg_win = np.mean(winners) if winners else 0
        avg_loss = np.mean(losers) if losers else 0

        if avg_loss != 0:
            win_loss_ratio = avg_win / abs(avg_loss)
        else:
            win_loss_ratio = 0
    else:
        hit_rate = 0.0
        avg_win = 0.0
        avg_loss = 0.0
        win_loss_ratio = 0.0

    return {
        "Annual Return": annual_return,
        "Annual Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
        "Hit Rate": hit_rate,
        "Total Trades": len(trades),
        "Avg Win": avg_win,
        "Avg Loss": avg_loss,
        "Win/Loss Ratio": win_loss_ratio
    }

