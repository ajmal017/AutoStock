from shell import RobinhoodShell

robinhood_shell = RobinhoodShell()


def add_new_price(price, symbol):
    desired_length = 5
    file = open(symbol + '.txt', 'r')
    prices = []
    for line in file:
        prices.append(float(line))
    if len(prices) >= desired_length:
        prices.pop(0)
    prices.append(float(price))
    file.close()

    file = open(symbol + '.txt', 'w')
    for price in prices:
        file.write(str(price) + '\n')
    file.close()


def get_price(symbol):
    instrument_url = robinhood_shell.get_instrument(symbol)['url']
    data = robinhood_shell.trader.get_stock_marketdata([instrument_url])
    return float(data[0]['last_trade_price'])


add_new_price(get_price('TSLA'), 'TSLA')
