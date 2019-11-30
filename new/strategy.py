from move import Move
from datetime import datetime, timedelta
import pandas_datareader.data as web


class Strategy:
    last_move = None
    prices = None
    days_back_length = 0

    @staticmethod
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
    def get_prices(symbol, start_date, end_date):
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

    def is_market_open(self, date):
        return not len(self.get_prices('DOW', date, date)) == 0

    def get_move(self, prices, index):
        return Move.HOLD
