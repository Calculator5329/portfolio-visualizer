import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


def dlr(val):
    return round(val * 100) / 100


def price_scrape(data):
    price_list = []
    for i in range(len(data)):
        price_list.append(dlr(data[i]))
    return price_list

def normalize(arr, start=0):
    for index, value in enumerate(arr):
        if index < start:
            pass
        if index == start:
            lastVal = arr[0]
            arr[0] = 100
            continue

        currentVal = arr[index]

        # noinspection PyUnboundLocalVariable
        arr[index] = (currentVal / lastVal) * arr[index - 1]

        lastVal = currentVal
    return arr



start_date = "2013-1-25"
end_date = "2023-1-25"


prices = {}
test_dict = {"JNJ": 50, "SOXL": 50}

for ticker in test_dict:
    print(ticker)
    stock = yf.Ticker(ticker)
    history = stock.history(start=start_date, end=end_date)
    prices[ticker] = price_scrape(history['Close'])

print(prices)

soxl_test = prices["SOXL"]

print(soxl_test[-1])
print(soxl_test[0])

print(normalize(soxl_test)[-1])
print(normalize(soxl_test)[0])

totals_list = []

firstKey = list(prices.keys())[0]

for value in prices[firstKey]:
    totals_list.append(0)

for ticker in prices:
    for index, value in enumerate(prices[ticker]):
        if index == 0:
            lastVal = prices[ticker][0]
            prices[ticker][0] = 100
            continue

        currentVal = prices[ticker][index]

        # noinspection PyUnboundLocalVariable
        prices[ticker][index] = (currentVal / lastVal) * prices[ticker][index - 1]

        lastVal = currentVal

for ticker in prices:
    for index, value in enumerate(prices[ticker]):
        totals_list[index] += (value * test_dict[ticker] / 100)

print(totals_list)

df = pd.DataFrame(totals_list)

df.plot()

plt.show()