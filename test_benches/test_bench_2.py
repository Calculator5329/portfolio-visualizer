def portfolio_value(prices, shares):
    out = []
    for i in range(len(prices)):
        out.append(prices[i] * shares[i])
    return out


def generic_combine(arr1, arr2):
    out = []
    for i in range(len(arr1)):
        out.append(arr1[i] + arr2[i])
    return out


stock_one = [100, 120, 140, 130, 150, 145, 165, 155]
stock_two = [100, 80, 75, 60, 80, 120, 160, 175]

shares_one = [10]
shares_two = [10]

stock_one_weight = 0.5
stock_two_weight = 0.5

addition = 10


print(shares_one)

for index in range(len(stock_one)-1):
    # Total portfolio value * weight / current price

    rebalance_freq = 2

    if index % rebalance_freq == 0 and index is not 0:

        shares_one.append(((stock_one[index + 1] * shares_one[index] + stock_two[index + 1] * shares_two[index]) *
                            stock_one_weight) / stock_one[index + 1] +
                            addition * stock_one_weight / stock_one[index + 1])
        shares_two.append(((stock_one[index + 1] * shares_one[index] + stock_two[index + 1] * shares_two[index]) *
                            stock_one_weight) / stock_two[index + 1] +
                            addition * stock_two_weight / stock_two[index + 1])

    else:
        shares_one.append(shares_one[index])
        shares_two.append(shares_two[index])



print(f"Prices one: {stock_one}")
print(f"Prices two: {stock_two}")
print("")

print(f"Shares one: {shares_one}")
print(f"Shares two: {shares_two}")
print("")

portfolio_one = portfolio_value(stock_one, shares_one)
portfolio_two = portfolio_value(stock_two, shares_two)

print(f"Portfolio one: {portfolio_one}")
print(f"Portfolio two: {portfolio_two}")
print("")

print(f"Combined Portfolio: {generic_combine(portfolio_one, portfolio_two)}")


