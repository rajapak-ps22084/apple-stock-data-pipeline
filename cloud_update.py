"""
cloud_update.py

A one-shot version of the update+visualize pipeline, built for GitHub Actions.

app.py is designed to run forever on your own machine (schedule + while True),
which doesn't work in GitHub Actions (each run starts fresh and must finish).
This script does the same data fetch + chart generation, but runs once and exits,
so a scheduled GitHub Actions workflow can call it daily.

Your local app.py and visualize.py are untouched and still work exactly as before
if you want to run the pipeline continuously on your own computer.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def update_stock_data():
    print("Starting data update process...")
    ticker_symbol = "AAPL"
    stock_data = yf.Ticker(ticker_symbol)
    hist = stock_data.history(period="3mo")

    if hist.empty:
        raise ValueError("No data received from Yahoo Finance.")

    conn = sqlite3.connect("Stock_Project.db")
    hist.to_sql("apple_stocks", conn, if_exists="replace", index=True)
    conn.close()
    print("Success: Stock data updated in the SQLite database!")


def generate_chart():
    conn = sqlite3.connect("Stock_Project.db")
    df = pd.read_sql("SELECT * FROM apple_stocks", conn, index_col="Date")
    conn.close()

    plt.figure(figsize=(10, 5))
    plt.plot(
        pd.to_datetime(df.index),
        df["Close"],
        label="Apple Close Price",
        color="blue",
        linewidth=2,
    )
    plt.title("Apple Stock Price (Last 3 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("apple_stock_graph.png", dpi=300)
    print("Graph saved successfully as apple_stock_graph.png!")


if __name__ == "__main__":
    update_stock_data()
    generate_chart()
