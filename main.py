import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


# Functions

def dlr(val):
    return round(val * 100) / 100


def validate_int_input(firstString, errorString="Error, please enter an integer: "):
    validatedInput = 0
    tryLoop = True

    try:
        validatedInput = int(input(firstString))
    except ValueError:
        while tryLoop:
            tryLoop = False
            try:
                validatedInput = int(input(errorString))
            except ValueError:
                tryLoop = True
    return validatedInput


def validate_str_input(firstString, errorString="Error, please enter a string: "):
    validatedInput = ""
    tryLoop = True

    try:
        validatedInput = str(input(firstString))
    except ValueError:
        while tryLoop:
            tryLoop = False
            try:
                validatedInput = str(input(errorString))
            except ValueError:
                tryLoop = True
    return validatedInput


def price_scrape(data):
    price_list = []
    for i in range(len(data)):
        price_list.append(dlr(data[i]))
    return price_list


def normalize(arr, start=0):
    for index, value in enumerate(arr):
        if index < start:
            continue
        if index == start:
            lastVal = arr[start]
            arr[start] = 100
            continue

        currentVal = arr[index]

        # noinspection PyUnboundLocalVariable
        arr[index] = (currentVal / lastVal) * arr[index - 1]

        lastVal = currentVal
    return arr


def average(arr):
    return dlr(sum(arr) / len(arr))


def getUserInput():
    userStartYear = validate_int_input("Enter the year you would like the backtest to begin: ",
                                       "Error, please enter a valid year: ")
    # userStartYear = 2015

    start_date = str(userStartYear) + "-1-1"
    end_date = "2023-1-28"

    # Dictionary for the portfolio
    tickers_weights = {}
    ticker_weights_sum = sum(list(tickers_weights.values()))

    ticker_input = validate_str_input("Enter a ticker to add to your portfolio (press enter to exit): ")

    while ticker_input not in ["", " ", "  ", "   ", "exit"] and ticker_weights_sum != 100:
        print(ticker_weights_sum)
        weight_input = validate_int_input("Enter a weight (1-100): ")

        while weight_input > 100 or weight_input < 1:
            weight_input = validate_int_input("Please enter a weight between 1 and 100: ")

        tickers_weights[ticker_input] = weight_input
        current_weight_input = weight_input
        ticker_weights_sum = sum(list(tickers_weights.values()))

        if ticker_weights_sum == 100:
            continue

        if ticker_weights_sum > 100:

            portfolio_weight_message = f"Your total portfolio weight cannot exceed 100.\nPress r to reset weights or " \
                                       f"press c to continue with your current portfolio \nYour last entered holding will" \
                                       f" have a weight of " + str(100 - ticker_weights_sum
                                                                   + current_weight_input) + ".\n" \
                                                                                             "Enter response here: "

            portfolio_weight_input = validate_str_input(portfolio_weight_message)

            if portfolio_weight_input.upper() in ["R", "RESET"]:
                tickers_weights = {}
                ticker_weights_sum = 0
                current_weight_input = 0
                ticker_input = validate_str_input("Enter a ticker to add to your portfolio (press enter to exit): ")
                continue

            if portfolio_weight_input.upper() in ["C", "CONTINUE", "CURRENT"]:
                tickers_weights[ticker_input] = (100 - ticker_weights_sum) + current_weight_input
                ticker_weights_sum = 100
                continue
        else:
            ticker_input = validate_str_input("Enter a ticker to add to your portfolio (press enter to exit): ")

    print("\nYour Portfolio:")

    for ticker in tickers_weights:
        print(f"{ticker.upper()}: {tickers_weights[ticker]}%")
    print("")

    return tickers_weights


# Portfolio Class
class Portfolio:

    def __init__(self, tickers_weights):
        self.shares = {}
        self.portfolio_value = []
        self.tickers_weights = tickers_weights
        self.start_date = "2012-12-31"
        self.end_date = "2022-12-31"
        self.prices = {}

    def initialize_tickers(self):
        for ticker in self.tickers_weights:
            # Pull data from yfinance and take the price history data
            stock = yf.Ticker(ticker)
            history = stock.history(start=self.start_date, end=self.end_date)
            self.prices[ticker] = price_scrape(history['Open'])

    def calculate_portfolio(self, initial_investment, addition):
        # Keep track of how many shares owned for each company by initializing self.shares with inital buy of shares
        for ticker in self.prices:
            new_shares = (initial_investment * self.tickers_weights[ticker] / 100) / 100
            self.shares[ticker] = [new_shares]

        # We have self.prices formatted something like this: {"VTI" : [prices], "QQQ" : [prices]}
        # First we run through and make sure the price lists begin at 100 for equal comparisons

        for ticker in self.prices:
            self.prices[ticker] = normalize(self.prices[ticker])

        firstKey = list(self.prices.keys())[0]

        # Looping through prices
        for i in range(len(self.prices[firstKey])):
            adjustedValue = 0

            # Looping through tickers
            for ticker in self.prices:
                # Normally, the share count should just be the same as "yesterday"
                self.shares[ticker].append(self.shares[ticker][-1])

                # Contribution frequency, set to one month by default
                contribute_freq = 300000

                # Rebalance frequency, set to one month by default
                rebalance_freq = 30

                # Rebalancing
                if i % rebalance_freq == 0 and not i == 0:
                    # Rebalances by adjusting share count to: Total portfolio value * weight / current price

                    total_portfolio_value = self.portfolio_value[-1]
                    weight = self.tickers_weights[ticker] / 100
                    current_price = self.prices[ticker][i]

                    self.shares[ticker][-1] = (total_portfolio_value * weight) / current_price

                # Add shares proportional to "addition" whenever its time to buy more
                if i % contribute_freq == 0 and not i == 0:
                    weight = self.tickers_weights[ticker] / 100
                    current_price = self.prices[ticker][i]
                    self.shares[ticker][-1] += (addition * weight) / current_price
                # Add this holdings value to the current portfolio value
                adjustedValue += self.prices[ticker][i] * self.shares[ticker][i]

            # Add the final portfolio value to portfolio_value list
            self.portfolio_value.append(adjustedValue)

    def get_end_value(self):
        return self.portfolio_value[-1]

    def get_shares(self):
        return self.shares

    def get_portfolio(self):
        return self.portfolio_value

    def get_prices(self):
        return self.prices

    def set_start_date(self, start_date_):
        self.start_date = start_date_

    def set_end_date(self, end_date_):
        self.end_date = end_date_


# Get user input
tickers_weights = getUserInput()

# Setting up the comparison portfolio
comparison = Portfolio(tickers_weights)

comparison.initialize_tickers()

comparison.calculate_portfolio(initial_investment=1000, addition=500)

print(f"Starting portfolio value: {comparison.get_portfolio()[0]}")
print(f"Ending portfolio value: {comparison.get_portfolio()[-1]}")


# Display as a chart
df = pd.DataFrame(comparison.get_portfolio())

df.plot()

plt.show()

"""
           # Initialize the dictionary for storing share counts
        for ticker in self.prices:
            self.shares[ticker] = []

        for ticker in self.prices:
            currentShares = 0
            for index, value in enumerate(self.prices[ticker]):
                currentShares += addition / value
                self.shares[ticker][index] = currentShares

        """
