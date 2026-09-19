import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

conn = sqlite3.connect("Stock_Project.db")
df = pd.read_sql("SELECT * FROM apple_stocks", conn, index_col="Date")
conn.close()

print("Data read from database:")
print(df.head())


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
print("Graph saves successfully as apple_stock_graph.png!")

plt.show()