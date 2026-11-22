# Stock Portfolio Performance Tracker

A simple Python console program that tracks an investment portfolio. The user enters stock ticker symbols, buy prices and share quantities. The program calculates the total portfolio value, the gain/loss per holding and saves a summary log to a CSV file.

## Features

- Validates tickers against the S&P 500 dataset (sp500.csv)
- Fetches live prices using yfinance (manual price entry if live price is not available)
- Calculates invested amount, current value, gain/loss and gain/loss % for each stock
- Prints a formatted table with the total portfolio performance
- Appends every run to portfolio_summary.csv with a timestamp

## Project Structure

- portfolio.py: main program
- sp500.csv: S&P 500 ticker dataset
- portfolio_summary.csv: generated performance log

## Requirements

- Python 3
- yfinance (py -m pip install yfinance)

## How to Run

python portfolio.py

Enter the ticker, buy price and quantity for each stock. Type done instead of a ticker to finish.
