# Overview
This Python application is designed for backtesting investment strategies using real stock market data. It allows users to create a portfolio of stocks, specify investment amounts, and simulate the portfolio's performance over time. The application is built with Python and utilizes libraries like Pandas, Matplotlib, and Yahoo Finance (yfinance) for data processing and visualization.

# Features
Portfolio Simulation: Users can simulate the performance of a custom stock portfolio over a specified time period.

Data Visualization: The application generates a plot showing the portfolio value over time, providing a visual representation of investment performance.

User Input Validation: It includes robust input validation functions to ensure correct and meaningful user inputs.

Dynamic Data Retrieval: Retrieves and processes stock price data dynamically from Yahoo Finance.

# How to Use
Create Your Portfolio: Enter the ticker symbols of the stocks you want to include in your portfolio along with their respective weights.

Specify Investment Details: Input the starting year for the backtest, your initial investment, and monthly contributions.

Analyze the Performance: Observe the plotted chart showing the growth of your portfolio over the specified period.

# Requirements
Python 3.x

Libraries: Pandas, Matplotlib, yfinance

Internet connection for retrieving stock data from Yahoo Finance.

# Installation and Execution
To run the application, ensure Python 3.x is installed along with the required libraries. Clone or download the repository, navigate to the project directory, and execute the main script.

# Example Portfolio

__Inputs:__

50% Amazon, 50% Google

$1000 Initial investment, $100 Monthly contribution

2015-2023

__Results:__

![Screenshot_48](https://github.com/Calculator5329/portfolio-visualizer/assets/62777822/7df0a611-f244-4684-810c-82ad7908ee2d)

# Log

Enter your initial investment: $1000

Enter your monthly addition to the portfolio: $100

1 of 1 completed

Total Contributions: $10,600.00

Time Weighted Rate of Return: 7.83%

Starting portfolio value: $1,000.00

Ending portfolio value: $14,742.90
