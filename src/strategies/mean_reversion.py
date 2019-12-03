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

    # def get_best_intervals(self, symbol, start_date, end_date, minimum=1, maximum=200):
