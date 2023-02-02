

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
