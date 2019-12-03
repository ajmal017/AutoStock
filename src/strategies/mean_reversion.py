from strategy import Strategy
from statistics import mean
from move import Move


class MeanReversion(Strategy):

    def __init__(self, long_term_days_count, short_term_days_count):
        self.long_term_days_count = long_term_days_count
        self.short_term_days_count = short_term_days_count
        self.days_back_length = long_term_days_count

    def get_move(self, prices, last_move, index=-1):
        which_price = 'Adj Close'
        long_term_average = mean([price[which_price] for price in prices[index - self.long_term_days_count:index - 1]])
        short_term_average = mean([price[which_price] for price in prices[index - self.short_term_days_count:index - 1]])
        if short_term_average < long_term_average and last_move == Move.SELL:
            return Move.BUY
        elif short_term_average > long_term_average and last_move == Move.BUY:
            return Move.SELL
        else:
            return Move.HOLD

    def get_best_intervals(self, symbol, start_date, end_date, long_term_minimum=25, long_term_maximum=200, short_term_minimum=2, short_term_maximum=50):
        self.days_back_length = long_term_maximum  # to get prices far back enough
        prices = self.get_prices(symbol, start_date, end_date)
        best_intervals = None
        best_percent = None
        for long_term in range(long_term_minimum, long_term_maximum + 1):
            print(str(long_term - long_term_minimum + 1) + '/' + str(long_term_maximum - long_term_minimum + 1))
            short_term_maximum = short_term_maximum if short_term_maximum < long_term else long_term - 1
            for short_term in range(short_term_minimum, short_term_maximum + 1):
                self.long_term_days_count = long_term
                self.short_term_days_count = short_term
                percent = self.get_mock_percentage(0, 0, 0, prices=prices[abs(long_term_maximum - long_term):])
                if best_percent is None or percent > best_percent:
                    best_percent = percent
                    best_intervals = (long_term, short_term)
        print(best_percent)
        return best_intervals
