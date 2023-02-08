from audioop import mul
from distutils.util import change_root
from itertools import chain
import yfinance as yf
from datetime import datetime as dt


def dlr(val):
    return round(val * 100) / 100


def round_decimal(val, places=2):
    return round(val * 10 ** places) / 10 ** places


def product(arr):
    out = 1
    for i in arr:
        out *= i
    return out


def price_scrape(data):
    price_list = []
    for i in range(len(data)):
        price_list.append(dlr(data[i]))
    return price_list


def calc_days(start_day, end_day):
    date1 = dt.strptime(start_date, "%Y-%m-%d")
    date2 = dt.strptime(end_date, "%Y-%m-%d")
    return (date1-date2).days


def my_debug(msg, val):
    print(f"DEBUG MESSAGE: {msg}: {val}")


# Pull data from yfinance and take the price history data
ticker = "crsr"
stock = yf.Ticker(ticker)

start_date = "2020-01-01"
end_date = "2023-01-01"

history = stock.history(start=start_date, end=end_date)
prices = {}
prices[ticker] = price_scrape(history['Open'])


def calculate_portfolio_changes(stock_dict, weights):
    # Convert the dictionary to a list of lists
    stock_list = []
    for stock in stock_dict.keys():
        stock_list.append(stock_dict[stock])

    lengths = []
    for i in stock_dict.keys():
        lengths.append(len(stock_dict[i]))

    desired_length = max(lengths)

    stock_changes = [[] for stock in stock_list]
    weights_list = [[] for i in range(desired_length - 2)]

    for index, stock in enumerate(stock_list):

        stock_len = len(stock)

        # Add blank change values for before the stock went IPO
        if desired_length > stock_len:
            for i in range(desired_length - len(stock)):
                stock_changes[index].append(None)
                stock.insert(0, 0)

        # Record % changes in stock price
        for i in range(len(stock) - 2):
            if stock[i] != 0:
                change = round_decimal((stock[i+1] / stock[i]), 4)
                stock_changes[index].append(change)

    for i in range(desired_length - 2):
        # Run through list of stocks
        for index, changes_list in enumerate(stock_changes):
            # If stock change exists we can use it, so we add its weight to the weights list
            if len(changes_list) > i:
                if changes_list[i]:
                    weights_list[i].append(weights[index])

    # Initialize price list with 100 as first value
    price_list = [100]
    rebalance_freq = 1

    for i in range(desired_length - 2):

        multiplier = 1
        current_weight_sum = 0

        for weight_index, j in enumerate(weights_list[i]):
            if i % rebalance_freq == 0 and i != 0:
                # If we are rebalancing, return to then normal weight
                weight = j / 100
            else:
                # Calculate total portfolio value
                total_portfolio = 0
                for k in range(len(stock_list) - 1):
                    total_portfolio += stock_list[k][i]

                # Calculate weight using price/portfolio
                weight = stock_list[weight_index][i] / total_portfolio

            # This is used later just in case we have an incomplete weights list
            current_weight_sum += weight
            price_change = stock_changes[weight_index][i] - 1
            multiplier += price_change * weight

            if current_weight_sum < 1:
                adjustment = 1 / current_weight_sum
                multiplier = abs(1 - multiplier) * adjustment + 1

        this_price = round_decimal(price_list[i] * multiplier)

        price_list.append(this_price)

    portfolio_changes = []
    my_debug("priceList", price_list)

    for index in range(len(price_list) - 1):
        change = round_decimal(
            price_list[index + 1] / price_list[index], 8)

        portfolio_changes.append(change)
            
    return [portfolio_changes, price_list]




my_stocks = {1 : [100, 101, 102, 103, 104, 105, 100, 100],
             2 :             [40, 44, 41,  43,   40, 40],
             3 :                        [34, 36, 34, 34]}

correct_response  = [100, 101, 102, 107.6, ]

my_weights = [33, 33, 34]

print(calculate_portfolio_changes(my_stocks, my_weights)[0])
print(calculate_portfolio_changes(my_stocks, my_weights)[1])

changes = [1.01, 1.0099009901, 1.0549019608, 1.0292750929, 1.0392776524, 0.8976542137]

initial = 1000
monthly = 500

# Contribution frequency, set to one month by default
contribute_freq = 3

# Rebalance frequency, set to one month by default
rebalance_freq = 3

portfolio_vals = [initial]

# for index, change in enumerate(changes):
    
    
