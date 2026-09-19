import time
import schedule
import sqlite3
import yfinance as tf


def update_stock_data():
  print("Starting data update process...")
  try:
  
    ticker_symbol = "AAPL"
    stock_data = tf.Ticker(ticker_symbol)
    hist = stock_data.history(period="3mo")

    if hist.empty:
      raise ValueError("No data received from Yahoo Finance.")

    conn = sqlite3.connect("Stock_Project.db")
    hist.to_sql("apple_stocks", conn, if_exists="replace", index=True)
    conn.close()

    print("Success: Stock data successfully updated in the SQLite database!")

  except Exception as e:
    print(f"Error occurred during update: {e}")


schedule.every().day.at("09:00").do(update_stock_data)

print(
    "Automated robust update system is running. Keep the terminal open to"
    " maintain the schedule..."
)

while True:
  schedule.run_pending()
  time.sleep(1)