# Optimization Module: Functions for parameter optimization via grid search.
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple

from strategy.strategy import run_strategy


def perform_grid_search(
    data: pd.DataFrame,
    threshold: float,
    decel_rate: float,
    step: float = 0.05,
    macro_df: Optional[pd.DataFrame] = None
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Finds optimal Alpha/Beta parameters based on Sharpe Ratio.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Price data with 'Close' column
    threshold : float
        Crossover threshold for entry signals
    decel_rate : float
        Deceleration rate for exit signals
    step : float
        Step size for parameter grid search
    macro_df : pd.DataFrame, optional
        Macroeconomic signals DataFrame
    
    Returns:
    --------
    Tuple[pd.DataFrame, Dict]
        (heatmap_data, best_params)
    """
    r = np.arange(step, 1.0, step)
    results = []

    print(f"Scanning parameters (Step: {step})...")

    best_sharpe = -np.inf
    best_params = {}

    for alpha in r:
        for beta in r:
            if alpha >= beta:
                continue

            metrics, _, _ = run_strategy(
                data, alpha, beta,
                threshold=threshold,
                decel_rate=decel_rate,
                macro_df=macro_df
            )

            results.append({
                'alpha': round(alpha, 2),
                'beta': round(beta, 2),
                'Sharpe': metrics['Sharpe Ratio']
            })

            if metrics['Sharpe Ratio'] > best_sharpe:
                best_sharpe = metrics['Sharpe Ratio']
                best_params = {'alpha': alpha, 'beta': beta}

    results_df = pd.DataFrame(results)
    heatmap_data = results_df.pivot(index='alpha', columns='beta', values='Sharpe')

    return heatmap_data, best_params

