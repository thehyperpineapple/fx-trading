"""
Streamlit Trading Strategy Backtesting Application
===================================================
Interactive web application for backtesting trading strategies.
"""

import streamlit as st
import pandas as pd
from strategy import run_backtest
from strategy.visualization import plot_heatmap, plot_trades
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Trading Strategy Backtester",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Trading Strategy Backtester")
st.markdown("""
This application allows you to backtest a trading strategy using exponential smoothing indicators
with optional macroeconomic variable integration.
""")

# Sidebar for inputs
st.sidebar.header("Strategy Parameters")

# Input fields
ticker = st.sidebar.text_input(
    "Ticker Symbol",
    value="EURUSD=X",
    help="Enter the ticker symbol (e.g., EURUSD=X for FX pairs)"
)

col1, col2 = st.sidebar.columns(2)

start_date = col1.date_input(
    "Start Date",
    value=pd.to_datetime("2024-01-01").date(),
    help="Select the start date for backtesting"
)

end_date = col2.date_input(
    "End Date",
    value=pd.to_datetime("2025-01-01").date(),
    help="Select the end date for backtesting"
)

threshold = st.sidebar.number_input(
    "Threshold",
    value=0.00015,
    min_value=0.0,
    max_value=1.0,
    step=0.00005,
    format="%.5f",
    help="Crossover threshold for entry signals"
)

deceleration_rate = st.sidebar.number_input(
    "Deceleration Rate",
    value=0.0005,
    min_value=0.0,
    max_value=1.0,
    step=0.0001,
    format="%.4f",
    help="Deceleration rate for exit signals"
)

initial_capital = st.sidebar.number_input(
    "Initial Capital ($)",
    value=10000.0,
    min_value=1000.0,
    max_value=1000000.0,
    step=1000.0,
    help="Starting capital for the strategy"
)

use_macro = st.sidebar.checkbox(
    "Use Macroeconomic Variables",
    value=False,
    help="Enable macroeconomic variable filtering for entry signals"
)

grid_search_step = st.sidebar.slider(
    "Grid Search Step Size",
    min_value=0.01,
    max_value=0.1,
    value=0.05,
    step=0.01,
    help="Step size for parameter optimization (smaller = more thorough but slower)"
)

# Run button
run_button = st.sidebar.button("Run Backtest", type="primary", use_container_width=True)

# Main content area
if run_button:
    # Validate inputs
    if start_date >= end_date:
        st.error("Start date must be before end date!")
        st.stop()
    
    # Convert dates to strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Show progress
    with st.spinner("Running backtest"):
        try:
            # Run backtest
            results = run_backtest(
                ticker=ticker,
                start_date=start_date_str,
                end_date=end_date_str,
                threshold=threshold,
                deceleration_rate=deceleration_rate,
                use_macro=use_macro,
                initial_capital=initial_capital,
                grid_search_step=grid_search_step,
                plot_results=False 
            )
            
            # Display success message
            st.success("Backtest completed successfully!")
            
            # Display optimal parameters
            st.header("ptimal Parameters")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Alpha (Slow)", f"{results['best_params']['alpha']:.4f}")
            with col2:
                st.metric("Beta (Fast)", f"{results['best_params']['beta']:.4f}")
            
            # Display performance metrics
            st.header("Performance Metrics")
            
            metrics = results['metrics']
            
            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Annual Return",
                    f"{metrics['Annual Return']:.2%}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Sharpe Ratio",
                    f"{metrics['Sharpe Ratio']:.4f}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "Max Drawdown",
                    f"{metrics['Max Drawdown']:.2%}",
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Hit Rate",
                    f"{metrics['Hit Rate']:.2%}",
                    delta=None
                )
            
            # Additional metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
            
            with col2:
                st.metric("Total Trades", f"{metrics['Total Trades']}")
            
            with col3:
                st.metric("Avg Win", f"${metrics['Avg Win']:.6f}")
            
            with col4:
                st.metric("Avg Loss", f"${metrics['Avg Loss']:.6f}")
            
            # Win/Loss Ratio
            st.metric("Win/Loss Ratio", f"{metrics['Win/Loss Ratio']:.2f}")
            
            # Detailed metrics table
            with st.expander("📋 Detailed Metrics Table"):
                metrics_df = pd.DataFrame([metrics]).T
                metrics_df.columns = ['Value']
                st.dataframe(metrics_df, use_container_width=True)
            
            # Visualizations
            st.header("Visualizations")
            
            # Heatmap
            st.subheader("Sharpe Ratio Heatmap")
            fig_heatmap = plot_heatmap(results['heatmap_data'], show_plot=False)
            st.pyplot(fig_heatmap)
            plt.close(fig_heatmap)
            
            # Trades and Equity Curve
            st.subheader("Price, Indicators & Equity Curve")
            fig_trades = plot_trades(results['strategy_df'], results['trades_df'], show_plot=False)
            st.pyplot(fig_trades)
            plt.close(fig_trades)
            
            # Trade log table
            if not results['trades_df'].empty:
                st.subheader("Trade Log")
                st.dataframe(results['trades_df'], use_container_width=True)
                
                # Download button for trade log
                csv = results['trades_df'].to_csv(index=False)
                st.download_button(
                    label="Download Trade Log CSV",
                    data=csv,
                    file_name=f"trade_log_{ticker}_{start_date_str}_{end_date_str}.csv",
                    mime="text/csv"
                )
            
            # Store results in session state for potential future use
            st.session_state['last_results'] = results
            
        except Exception as e:
            st.error(f"Error running backtest: {str(e)}")
            st.exception(e)

else:
    # Show instructions when app first loads
    st.info("Please configure the parameters in the sidebar and click 'Run Backtest' to start.")
    
    # Show example configuration
    with st.expander("ℹExample Configuration"):
        st.markdown("""
        **Recommended starting parameters:**
        - **Ticker**: EURUSD=X
        - **Start Date**: 2024-01-01
        - **End Date**: 2025-01-01
        - **Threshold**: 0.00015
        - **Deceleration Rate**: 0.0005
        - **Initial Capital**: $10,000
        - **Use Macro**: False (for faster initial testing)
        - **Grid Search Step**: 0.05
        
        **Note**: Using macroeconomic variables will fetch data from FRED and may take longer.
        Smaller grid search step sizes provide more thorough optimization but take longer to compute.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Trading Strategy Backtesting System | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

