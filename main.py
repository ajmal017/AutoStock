from shell import RobinhoodShell
from enum import Enum

robinhood_shell = RobinhoodShell()


class Action(Enum):
    BUY = 'buy'
    SELL = 'sell'
    HOLD = 'hold'


def get_prices_file(symbol):
    return 'data/' + symbol + '/prices.txt'


def get_last_action_file(symbol):
    return 'data/' + symbol + '/last-action.txt'


def set_last_action(symbol, action):
    file = open(get_last_action_file(symbol), 'w')
    file.write(action)
    file.close()


def add_new_price(price, symbol):
    file = open(get_prices_file(symbol), 'a')
    file.write('\n' + str(price))
    file.close()


def get_current_price(symbol):
    instrument_url = robinhood_shell.get_instrument(symbol)['url']
    data = robinhood_shell.trader.get_stock_marketdata([instrument_url])
    return float(data[0]['last_trade_price'])


def get_average(symbol, price_count):
    file = open(get_prices_file(symbol), 'r')
    all_prices = []
    for line in file:
        all_prices.append(float(line))
    file.close()
    prices = all_prices[-price_count:]
    return sum(prices) / len(prices)


def get_last_action(symbol):
    file = open(get_last_action_file(symbol), 'r')
    action = None
    for line in file:
        action = line
    file.close()
    return action


def get_action(symbol, price_count):
    price = get_current_price(symbol)
    average = get_average(symbol, price_count)
    last_action = get_last_action(symbol)
    if price > average and last_action == 'sell':
        return Action.BUY
    elif price < average and last_action == 'buy':
        return Action.SELL
    else:
        return Action.HOLD


def buy(symbol, quantity):
    instrument = robinhood_shell.get_instrument(symbol)
    robinhood_shell.trader.place_buy_order(instrument, quantity)
    set_last_action(symbol, 'buy')
    print(f'bought {quantity} share(s) of {symbol}')


def sell(symbol, quantity):
    instrument = robinhood_shell.get_instrument(symbol)
    robinhood_shell.trader.place_sell_order(instrument, quantity)
    set_last_action(symbol, 'sell')
    print(f'sold {quantity} share(s) of {symbol}')


def is_market_open():
    return False


def main(symbol, quantity, price_count):
    action = get_action(symbol, price_count)
    if action == Action.BUY:
        buy(symbol, quantity)
    elif action == Action.SELL:
        sell(symbol, quantity)


if __name__ == '__main__':
    main(symbol='GRPN', quantity=3, price_count=5)
