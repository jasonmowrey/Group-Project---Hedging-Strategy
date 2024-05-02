import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.stats import norm

# Function to fetch data
def fetch_data(tickers):
    data = yf.download(tickers, start="2021-01-01", end="2024-01-01")
    return data['Adj Close']

# Forecast returns using a basic statistical model
def forecast_returns(returns, days=730):
    mean_returns = returns.mean()
    std_dev_returns = returns.std()
    forecasts = np.random.normal(mean_returns, std_dev_returns, (days, len(returns.columns)))
    return pd.DataFrame(forecasts, columns=returns.columns)

# Update the graph and options details
def update(tickers_entry, root):
    tickers = tickers_entry.get().split(',')
    data = fetch_data(tickers)
    returns = data.pct_change().dropna()

    # Forecast future returns and calculate portfolio value
    forecasted_returns = forecast_returns(returns)
    forecasted_portfolio = (forecasted_returns + 1).cumprod()
    forecasted_portfolio['Portfolio Value'] = forecasted_portfolio.dot(np.ones(len(tickers)) / len(tickers))

    # Graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(forecasted_portfolio.index, forecasted_portfolio['Portfolio Value'], label='Forecasted Portfolio Value')
    ax.set_title('Forecasted Portfolio Performance')
    ax.set_xlabel('Days')
    ax.set_ylabel('Portfolio Value')
    ax.legend()

    # Clear previous figure
    for widget in root.pack_slaves():
        widget.destroy()

    # Embedding matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Display options needed for hedging
    options_frame = tk.Frame(root)
    options_frame.pack(side=tk.BOTTOM)
    tk.Label(options_frame, text="Options Needed for Hedging:", font=('Arial', 14)).pack(side=tk.TOP)
    for ticker in tickers:
        # Assuming 1 put option per 100 shares for simplicity
        tk.Label(options_frame, text=f"Buy put options for {ticker}: 100").pack()

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title('Portfolio Forecast and Hedging Details')

    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.TOP)
    tk.Label(input_frame, text="Enter stock tickers separated by comma:", font=('Arial', 12)).pack(side=tk.LEFT)
    tickers_entry = tk.Entry(input_frame)
    tickers_entry.pack(side=tk.LEFT)
    submit_button = tk.Button(input_frame, text="Submit", command=lambda: update(tickers_entry, root))
    submit_button.pack(side=tk.LEFT)

    root.mainloop()

# Main function to run the application
def main():
    create_gui()

if __name__ == '__main__':
    main()