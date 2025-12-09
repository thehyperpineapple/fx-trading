"""
Visualization Module
====================
Functions for plotting strategy results.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_heatmap(heatmap_data: pd.DataFrame, show_plot: bool = True):
    """
    Plot Sharpe Ratio heatmap.
    
    Parameters:
    -----------
    heatmap_data : pd.DataFrame
        Pivoted DataFrame with alpha as index, beta as columns, Sharpe as values
    show_plot : bool
        Whether to show the plot (default: True). Set to False for Streamlit.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="RdYlGn", center=0)
    plt.title("Strategy Sharpe Ratio Heatmap")
    plt.ylabel("Alpha (Slow)")
    plt.xlabel("Beta (Fast)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    if show_plot:
        plt.show()
    return plt.gcf()


def plot_trades(df: pd.DataFrame, trades_df: pd.DataFrame, show_plot: bool = True):
    """
    Plot price, indicators, trades, and equity curve.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Strategy DataFrame with price, indicators, and equity
    trades_df : pd.DataFrame
        DataFrame with trade log (Date, Type, Price columns)
    show_plot : bool
        Whether to show the plot (default: True). Set to False for Streamlit.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [2, 1]})

    # Plot 1: Price and Signals
    ax1.plot(df.index, df['Close'], label='Price', color='black', alpha=0.3)
    ax1.plot(df.index, df['es_slow'], label='ES Slow', color='blue', alpha=0.6)
    ax1.plot(df.index, df['es_fast'], label='ES Fast', color='orange', alpha=0.6)

    if not trades_df.empty:
        buys = trades_df[trades_df['Type'] == 'Buy']
        if not buys.empty:
            ax1.scatter(buys['Date'], buys['Price'], marker='^', color='green', s=100, label='Buy', zorder=5)

        sells = trades_df[trades_df['Type'] == 'Sell']
        if not sells.empty:
            ax1.scatter(sells['Date'], sells['Price'], marker='v', color='red', s=100, label='Sell', zorder=5)

    ax1.set_title("Price, Indicators & Trades")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Equity Curve
    ax2.plot(df.index, df['Equity'], color='purple', label='Strategy Equity')
    ax2.set_title("Equity Curve")
    ax2.set_ylabel("Account Balance ($)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    if show_plot:
        plt.show()
    return fig
