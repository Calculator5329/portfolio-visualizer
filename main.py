import datetime

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime as dt

# Functions

def my_debug(msg, val):
    print(f"DEBUG MESSAGE: {msg}: {val}")

def dlr(val):
    return round(val * 100) / 100

def round_decimal(val, places=2):
    return round(val * 10 ** places) / 10 ** places

def calc_days(start_day, end_day):
    date1 = dt.strptime(start_day, "%Y-%m-%d")
    date2 = dt.strptime(end_day, "%Y-%m-%d") 
    return abs((date1-date2).days)


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


def arrange_arr(arr, vals):
    return [x for _, x in sorted(zip(vals, arr), key=lambda pair: pair[0], reverse=True)]

def product(arr):
    out = 1
    for i in arr:
        out *= i
    return out


def getUserInput():
    # Dictionary for the portfolio
    tickers_weights = {}
    ticker_weights_sum = sum(list(tickers_weights.values()))

    ticker_input = validate_str_input("Enter a ticker to add to your portfolio (press enter to exit): ")

    while ticker_input not in ["", " ", "  ", "   ", "exit"] and ticker_weights_sum != 100:
        # print(ticker_weights_sum)
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
        self.portfolio_changes = []
        self.rebalance_freq = 30
        self.contribution_freq = 30

    def initialize_tickers(self):
        for ticker in self.tickers_weights:
            # Pull data from yfinance and take the price history data
            stock = yf.Ticker(ticker)
            history = stock.history(start=self.start_date, end=self.end_date)
            self.prices[ticker] = price_scrape(history['Open'])
        
    def calculate_portfolio_changes(self):
        # Convert the dictionary to a list of lists
        stock_list = []
        weights = []
        lengths = []
        for stock in self.prices.keys():
            stock_list.append(self.prices[stock])
            weights.append(tickers_weights[stock])
            lengths.append(len(self.prices[stock]))

        stock_list = arrange_arr(stock_list, lengths)
        
        desired_length = max(lengths)

        stock_changes = [[] for stock in stock_list]
        weights_list = [[] for i in range(desired_length - 1)]

        for index, stock in enumerate(stock_list):
            
            stock_len = len(stock)
            
            # Add blank change values for before the stock went IPO
            if desired_length > stock_len:
                for i in range(desired_length - stock_len):
                    stock_changes[index].append(None)
                    stock.insert(0, 0)
                i = desired_length - stock_len + 1
                while i < desired_length -1 :
                    stock_changes[index].append( round_decimal((stock[i+1] / stock[i]), 4))
                    i += 1
                i = 0
            else:               
                # my_debug("stock", stock)
            
                # Record % changes in stock price            
                for i in range(stock_len - 2):                
                    if stock[i] != 0 and stock[i + 1] != 0:
                        change = round_decimal((stock[i+1] / stock[i]), 4)
                        stock_changes[index].append(change)
                    else:
                        stock_changes[index].append(None)
                
            # my_debug("len(stock)", stock_len)
            
        # my_debug("stock_changes",stock_changes)


        for i in range(desired_length - 2):
            # Run through list of stocks
            for index, changes_list in enumerate(stock_changes):
                # If stock change exists we can use it, so we add its weight to the weights list
                if changes_list[i]:
                    weights_list[i].append(weights[index])
        
        # my_debug('wl', weights_list)
        
        # Initialize price list with 100 as first value
        price_list = [100]
        rebalance_freq = 1
        
        # my_debug("weightslist", weights_list)
        
        for i in range(desired_length - 1):
            
            multiplier = 1
            current_weight_sum = 0
    
            for weight_index, j in enumerate(weights_list[i]):
                if i % rebalance_freq == 0 and i != 0:
                    # If we are rebalancing, return to then normal weight
                    weight = j / 100
                else:
                    # Calculate total portfolio value
                    total_portfolio = 0
                    for k in range(len(stock_list)):
                        total_portfolio += stock_list[k][i]
            
                    # Calculate weight using price/portfolio
                    weight = stock_list[weight_index][i] / total_portfolio
        
                # This is used later just in case we have an incomplete weights list
                current_weight_sum += weight
                try:
                    price_change = stock_changes[weight_index][i] - 1
                except TypeError:
                    price_change = 0
                multiplier += price_change * weight
    
            # Check if current weight sum is less than 1 and adjust the multiplier if necessary
            if current_weight_sum < 1 and current_weight_sum != 0:
                adjustment = 1 / current_weight_sum
                multiplier = (multiplier -1) * adjustment + 1
            
            this_price = round_decimal(price_list[i] * multiplier)
            
            price_list.append(this_price) 

        for index in range(len(price_list) - 1):
            change = round_decimal(price_list[index + 1] / price_list[index], 8)
            self.portfolio_changes.append(change)

    def calculate_portfolio(self, initial_investment, addition):
        
        currentVal = initial_investment
        self.portfolio_value.append(initial_investment)
        
        for index, value in enumerate(self.portfolio_changes):
            workingVal = currentVal * value 
            
            if index != 0 and index % self.contribution_freq == 0:
                workingVal += addition
            
            currentVal = workingVal         
        
            # Add the final portfolio value to portfolio_value list
            self.portfolio_value.append(currentVal)

    def get_end_value(self):
        return self.portfolio_value[-1]

    def get_shares(self):
        return self.shares

    def get_portfolio(self):
        return self.portfolio_value

    def get_prices(self):
        return self.prices

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_changes(self):
        return self.portfolio_changes

    def set_start_date(self, start_date_):
        self.start_date = start_date_

    def set_end_date(self, end_date_):
        self.end_date = end_date_


debug_mode = False

# Get user input
if debug_mode:
    tickers_weights = {"META" : 22, "CRSR" : 16, "PINS" : 13, "DBX" : 14, "CRCT" : 10, "AMZN" : 9, "SNBR" : 7, "BABA" : 5, "PYPL" : 4}
else:
    tickers_weights = getUserInput()

# Setting up the comparison portfolio
comparison = Portfolio(tickers_weights)

userStartYear = validate_int_input("Enter the year you would like the backtest to begin: ",
                                   "Error, please enter a valid year: ")
# userStartYear = 2015
start_date = str(userStartYear) + "-1-1"
end_date = "2023-1-1"

comparison.set_start_date(start_date)
comparison.set_end_date(end_date)

comparison.initialize_tickers()
comparison.calculate_portfolio_changes()

# print(product(comparison.get_changes()))

user_initial = validate_int_input("Enter your initial investment: $")
user_addition = validate_int_input("Enter your monthly addition to the portfolio: $")

total_invested = user_initial + user_addition * 12 * (2023 - userStartYear)

comparison.calculate_portfolio(initial_investment=user_initial, addition=user_addition)

# print(comparison.get_portfolio())

# This data is only to set the dates, so I just used a random old company
data = yf.download("F", comparison.get_start_date(), comparison.get_end_date())
data["Portfolio_Value"] = comparison.get_portfolio()

portfolio_start_value = "$" + "{:,.2f}".format(comparison.get_portfolio()[0])

portfolio_end_value = "$" + "{:,.2f}".format(comparison.get_portfolio()[-1])

percent_gain = comparison.get_portfolio()[-1]  / total_invested
years_per_dollar = (2023 - userStartYear) * (user_initial / total_invested) + \
                  (2023 - userStartYear)/2 * ((total_invested - user_initial) / total_invested)
# print(years_per_dollar)
time_return = percent_gain**(1/years_per_dollar)
total_invested = "$" + "{:,.2f}".format(user_initial + user_addition * 12 * (2023 - userStartYear))
print("\n\n\n\n\n")
print(f"Total Contributions: {total_invested}\n")
print(f"TWRR: {str(round_decimal((time_return - 1) * 100))}%\n")
print(f"Starting portfolio value: " + portfolio_start_value)
print(f"Ending portfolio value: " + portfolio_end_value + "\n")

# Display as a chart
df = pd.DataFrame(data)

fig, ax = plt.subplots()

ax.plot(df["Portfolio_Value"])

ax.yaxis.set_major_formatter('${x:,.2f}')

fig.set_size_inches(16, 8)

plt.show()



'''




           # Initialize the dictionary for storing share counts
        for ticker in self.prices:
            self.shares[ticker] = []

        for ticker in self.prices:
            currentShares = 0
            for index, value in enumerate(self.prices[ticker]):
                currentShares += addition / value
                self.shares[ticker][index] = currentShares

    '''
