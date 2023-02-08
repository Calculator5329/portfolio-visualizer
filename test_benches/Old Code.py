

print("Welcome, this program backtests your portfolio and compares it with the overall market.\n")

# Defining ticker and historical range

try:
    user_input = input("Enter what ticker you would like to simulate returns for: ")
    stock = yf.Ticker(user_input)
except IndexError:
    user_input = input("Error, please enter a correctly formatted ticker (Ex: vti): ")
    stock = yf.Ticker(user_input)

userStartYear = validate_str_input("Enter the year you would like the backtest to begin: ")

start_date = userStartYear + "-2-13"
end_date = "2023-1-28"

# Initializing stock info
portfolio_hist = stock.history(start=start_date, end=end_date)

print(f"Downloading information for {user_input}")
data = yf.download(user_input, start_date, end_date)
print("")

# This code throws an error if yfinance can't find the entered ticker
try:
    tester = portfolio_hist["Open"][0]
except IndexError:
    print("\nCould not find specified ticker. Switching to default ticker 'VTI' ")
    stock = yf.Ticker("VTI")
    portfolio_hist = stock.history(start=start_date, end=end_date)

# Variables

monthly_addition = validate_int_input("Enter how much you would invest each month: ")

portfolio_price_list = []
portfolio_shares = 0
portfolio_values = {"Portfolio": [], "Comparison" : []}


comparison_stock = yf.Ticker("VTI")
comparison_price_list = []
comparison_hist = comparison_stock.history(start=start_date, end=end_date)


# Creating a clean price list
for i in range(len(portfolio_hist["Open"])):
    portfolio_price_list.append(dlr(portfolio_hist["Open"][i]))
    comparison_price_list.append(dlr(comparison_hist["Open"][i]))

# Creating the portfolio values list
for i in range(len(portfolio_price_list)):
    if i % 30 == 0:
        portfolio_shares += monthly_addition / portfolio_price_list[i]
    portfolio_values["Portfolio"].append(portfolio_shares * portfolio_price_list[i])

# Calculating end value of investments
end_value = portfolio_values[len(portfolio_values) - 1]

# Printing out results
print("Ending Portfolio Value: $" + str(dlr(end_value)))

# Adding the portfolio values data to the dataframe
data['Portfolio_Value'] = portfolio_values

df = pd.DataFrame(data)

df.plot(y="Portfolio_Value", kind="line")

plt.show()


'''
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
                contribute_freq = 30

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
                '''