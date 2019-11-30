from enum import Enum


class Action(Enum):
    BUY = 'buy'
    SELL = 'sell'
    HOLD = 'hold'


def get_prices_file(symbol):
    return 'mock-data/' + symbol + '/prices.txt'


def get_last_action_file(symbol):
    return 'mock-data/' + symbol + '/last-action.txt'


def get_last_action(symbol):
    file = open(get_last_action_file(symbol), 'r')
    action = None
    for line in file:
        action = line
    file.close()
    return action


def set_last_action(symbol, action):
    file = open(get_last_action_file(symbol), 'w+')
    file.write(action)
    file.close()


def get_prices(symbol):
    prices = []
    file = open(get_prices_file(symbol), 'r')
    for line in file:
        prices.append(float(line))
    file.close()
    return prices


def get_average(symbol, price_count, price_index):
    all_prices = get_prices(symbol)
    prices = all_prices[price_index - price_count:price_index]
    return sum(prices) / len(prices)


def get_current_price(symbol, price_index):
    all_prices = get_prices(symbol)
    return all_prices[price_index]


def get_action(symbol, price_count, price_index):
    price = get_current_price(symbol, price_index)
    average = get_average(symbol, price_count, price_index)
    last_action = get_last_action(symbol)
    if price > average and last_action == 'sell':
        return Action.BUY
    elif price < average and last_action == 'buy':
        return Action.SELL
    else:
        return Action.HOLD


def get_interest_with_program(symbol, price_count):
    initial_money = money = None
    shares = 0
    has_bought = False
    set_last_action(symbol, 'sell')
    for price_index in range(price_count + 1, len(get_prices(symbol))):
        action = get_action(symbol, price_count, price_index)
        if action == Action.BUY:
            if not has_bought:
                initial_money = money = get_current_price(symbol, price_index)
                has_bought = True
            money -= get_current_price(symbol, price_index)
            shares += 1
            set_last_action(symbol, 'buy')
        elif action == Action.SELL:
            money += get_current_price(symbol, price_index)
            shares -= 1
            set_last_action(symbol, 'sell')
    money += shares * get_prices(symbol)[-1]
    return ((money - initial_money) / money) * 100


def get_interest_without_program(symbol):
    prices = get_prices(symbol)
    initial_price = prices[0]
    end_price = prices[-1]
    return ((end_price - initial_price) / initial_price) * 100


def print_with_and_without(symbol, price_count):
    print(f'interest made with program: {format(get_interest_with_program(symbol, price_count), ".2f")}%')
    print(f'interest made without program: {format(get_interest_without_program(symbol), ".2f")}%')


def print_best(symbol, lower_bound, upper_bound):
    interests = []
    for i in range(lower_bound, upper_bound + 1):
        interests.append(get_interest_with_program(symbol, i))
    best = max(interests)
    print(f'best price count is {interests.index(best) + lower_bound} at {format(best, ".2f")}%')


def main():
    symbol = 'AAPL'
    print(format(get_interest_with_program(symbol, 5), '.2f'))
    print_best(symbol=symbol, lower_bound=1, upper_bound=25)
    print(f'interest made without program: {format(get_interest_without_program(symbol), ".2f")}%')


if __name__ == '__main__':
    main()
