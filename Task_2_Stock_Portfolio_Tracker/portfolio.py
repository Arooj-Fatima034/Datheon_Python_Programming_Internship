import csv
import os
from datetime import datetime

try:
    import yfinance as yf
except ImportError:
    yf = None


def load_tickers():
    tickers ={}
    with open("sp500.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tickers[row["Symbol"]] = row["Security"]
    return tickers


def get_price(symbol):
    try:
        data = yf.Ticker(symbol.replace(".", "-")).history(period="1d")
        return float(data["Close"].iloc[-1])
    except Exception:
        print("Live price for", symbol, "not found.")
        return float(input("Enter current price manually: "))


tickers = load_tickers()
portfolio = {}

print("Enter your stocks. Type 'done' instead of a ticker to finish.")
while True:
    symbol = input("Ticker symbol: ").upper()
    if symbol == "DONE":
        break
    if symbol not in tickers:
        print("This ticker is not in the S&P 500 list.")
        continue
    buy_price = float(input("Buy price: "))
    quantity = float(input("Shares quantity: "))
    portfolio[symbol] = [buy_price, quantity]

total_invested = 0
total_value = 0
rows = []
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print()
print("Symbol  Qty     Buy      Current  Invested   Value      Gain/Loss  %")
for symbol in portfolio:
    buy_price = portfolio[symbol][0]
    quantity = portfolio[symbol][1]
    current_price = get_price(symbol)

    invested = buy_price * quantity
    value = current_price * quantity
    gain = value - invested
    percent = gain / invested * 100

    total_invested += invested
    total_value += value

    print(f"{symbol:<7} {quantity:<7.2f} {buy_price:<8.2f} {current_price:<8.2f} {invested:<10.2f} {value:<10.2f} {gain:<10.2f} {percent:.2f}%")
    rows.append([now, symbol, tickers[symbol], quantity, buy_price, round(current_price, 2), round(invested, 2), round(value, 2), round(gain, 2), round(percent, 2)])

total_gain = total_value - total_invested
if total_invested > 0:
    total_percent = total_gain / total_invested * 100
    print()
    print("Total Invested :", round(total_invested, 2))
    print("Total Value    :", round(total_value, 2))
    print("Total Gain/Loss:", round(total_gain, 2), f"({total_percent:.2f}%)")
    rows.append([now, "TOTAL", "", "", "", "", round(total_invested, 2), round(total_value, 2), round(total_gain, 2), round(total_percent, 2)])
    file_exists = os.path.isfile("portfolio_summary.csv")
    with open("portfolio_summary.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Symbol", "Company", "Quantity", "Buy Price", "Current Price", "Invested", "Current Value", "Gain/Loss", "Gain/Loss %"])
        writer.writerows(rows)
    print("Summary saved to portfolio_summary.csv")
else:
    print("No stocks were entered.")
