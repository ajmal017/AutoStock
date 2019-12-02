from move import Move
from datetime import datetime, timedelta
import pandas_datareader.data as web


# ABSTRACT CLASS
class Strategy:
    # ABSTRACT VARIABLE
    # number of day prices before today that the API must fetch
    # for example, if the only historical data we need is yesterday's price, days_back_length = 1
    days_back_length = 0

    # ABSTRACT METHOD
    # returns Move.BUY, Move.SELL, or Move.HOLD
    def get_move(self, prices, last_move, index=-1):
        pass

    @staticmethod
    # date_string in format YYYY-MM-DD
    def get_datetime_object(date_string):
        nums = [int(i) for i in date_string.split('-')]
        date = datetime(nums[0], nums[1], nums[2])
        return date

    @staticmethod
    # returns a list of prices within inclusive range, each is a dictionary with the following keys:
    #   High
    #   Low
    #   Open
    #   Close
    #   Volume
    #   Adj Close
    def get_raw_prices(symbol, start_date, end_date):
        try:
            web_data = web.DataReader(symbol.upper(), 'yahoo', start_date, end_date)
        except KeyError:
            # KeyError means no data within date range
            return []
        prices = []
        i = 0
        # web_data is not iterable and has no len attribute, so we have to use this workaround
        while True:
            try:
                prices.append(web_data.iloc[i])
                i += 1
            except IndexError:
                break
        # the API includes one day past the end_date for some reason, so this fixes that
        if web_data.iloc[-1].name > end_date and len(prices) != 0:
            prices.pop()
        return prices

    # this method gives us days_back_length amount of day prices back, necessary because of days the market is closed
    def get_prices(self, symbol, start_date, end_date):
        # can probably reduce this number, especially with big date ranges
        multiplier = 4
        days_back_fetch = self.days_back_length * multiplier
        prices = self.get_raw_prices(symbol, start_date - timedelta(days=days_back_fetch), end_date)
        start_date_index = 0
        for i in range(len(prices)):
            if prices[i].name.date() >= start_date.date():
                start_date_index = i
                break
        if start_date_index != 0:
            return []
        return prices[start_date_index - self.days_back_length:]

    def is_market_open(self, date, symbol='DOW'):
        return len(self.get_raw_prices(symbol, date, date)) != 0

    def get_last_move(self, symbol):
        file = open('last_moves/' + str(self.__class__.__name__).lower() + '/' + symbol + '.txt', 'r')
        text = file.read()
        file.close()
        if text == 'buy':
            return Move.BUY
        elif text == 'sell':
            return Move.SELL

    def set_last_move(self, move, symbol):
        file = open('last_moves/' + str(self.__class__.__name__).lower() + '/' + symbol + '.txt', 'w+')
        if move == Move.BUY:
            file.write('buy')
        elif move == Move.SELL:
            file.write('sell')
        file.close()

    def get_mock_percentage(self, symbol, start_date, end_date):
        which_price = 'Adj Close'
        prices = self.get_prices(symbol, start_date, end_date)
        last_move = Move.SELL
        has_bought = False
        start_money = 0
        money = 0
        # don't need to keep track if we have a share or not because of last_move
        for i in range(self.days_back_length, len(prices)):
            move = self.get_move(prices, last_move, i)
            if move == Move.BUY and last_move == Move.SELL:
                if not has_bought:
                    start_money = prices[i][which_price]
                money = 0
                last_move = Move.BUY
            elif move == Move.SELL and last_move == Move.BUY:
                money = prices[i][which_price]
                last_move = Move.SELL
        if last_move == Move.BUY:
            money = prices[-1][which_price]
        percent = round((money - start_money) / start_money * 100, 2)
        return percent

    def get_hold_percentage(self, symbol, start_date, end_date):
        which_price = 'Adj Close'
        prices = self.get_prices(symbol, start_date, end_date)
        start_money = prices[self.days_back_length][which_price]
        end_money = prices[-1][which_price]
        percent = round((end_money - start_money) / start_money * 100, 2)
        print(start_money)
        print(end_money)
        return percent

    def get_current_move(self, symbol):
        now = datetime.now()
        if not self.is_market_open(now, symbol):
            return None
        prices = self.get_prices(symbol, now, now)
        last_move = self.get_last_move(symbol)
        move = self.get_move(prices, last_move)
        self.set_last_move(move, symbol)
        return move
