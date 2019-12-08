from strategy import Strategy
from statistics import mean
from move import Move


class MeanReversion(Strategy):

    def __init__(self, long_term_interval=90, short_term_interval=30):
        self.long_term_interval = long_term_interval
        self.short_term_interval = short_term_interval
        self.days_back_length = long_term_interval
        self.best_intervals = []  # made of tuples (long_term_interval, short_term_interval, percent)
        self.best_intervals_length = 100

    def get_move(self, prices, last_move, index=-1):
        which_price = 'Adj Close'
        long_term_average = mean([price[which_price] for price in prices[index - self.long_term_interval:index]])
        short_term_average = mean([price[which_price] for price in prices[index - self.short_term_interval:index]])
        if short_term_average < long_term_average and last_move == Move.SELL:
            return Move.BUY
        elif short_term_average > long_term_average and last_move == Move.BUY:
            return Move.SELL
        else:
            return Move.HOLD

    def do_best_intervals(self, symbol, start_date, end_date, directory, long_term_minimum=25, long_term_maximum=300, short_term_minimum=1, short_term_maximum=200):
        self.days_back_length = long_term_maximum  # to get prices far back enough
        prices = self.get_prices(symbol, start_date, end_date)
        original_short_term_maximum = short_term_maximum
        total_iterations = self.get_iteration_count(long_term_minimum, long_term_maximum, short_term_minimum, short_term_maximum)
        iterations = 0
        for long_term in range(long_term_minimum, long_term_maximum + 1):
            short_term_maximum = original_short_term_maximum
            short_term_maximum = short_term_maximum if short_term_maximum < long_term else long_term - 1
            for short_term in range(short_term_minimum, short_term_maximum + 1):
                iterations += 1
                print(str(iterations) + ' / ' + str(total_iterations))
                self.long_term_interval = long_term
                self.short_term_interval = short_term
                self.days_back_length = long_term
                percent = self.get_mock_percentage(0, 0, 0, prices=prices[long_term_maximum - long_term:])
                self.add_to_best(long_term, short_term, percent)
        self.write_to_file(directory, start_date, end_date, symbol)
        print('Done')

    @staticmethod
    def get_iteration_count(long_term_minimum, long_term_maximum, short_term_minimum, short_term_maximum):
        count = 0
        for long_term in range(long_term_minimum, long_term_maximum + 1):
            if long_term < short_term_maximum:
                count += long_term - short_term_minimum
            else:
                count += short_term_maximum - short_term_minimum + 1
        return count

    def add_to_best(self, long_term, short_term, percent):
        if len(self.best_intervals) < self.best_intervals_length:
            self.best_intervals.append((long_term, short_term, percent))
            self.best_intervals.sort(key=lambda x: x[-1], reverse=True)
        elif percent > self.best_intervals[-1][-1]:
            self.best_intervals.pop(-1)
            self.best_intervals.append((long_term, short_term, percent))
            self.best_intervals.sort(key=lambda x: x[-1], reverse=True)

    def write_to_file(self, directory, start_date, end_date, symbol):
        file = open(directory + '/' + str(start_date.date()) + '--' + str(end_date.date()) + '.txt', 'w+')
        file.write(str(start_date.date()) + ' - ' + str(end_date.date()) + '\n\n')
        file.write('long,short : percent%\n\n')
        for intervals in self.best_intervals:
            file.write(str(intervals[0]) + ',' + str(intervals[1]) + ' : ' + str(intervals[2]) + '%\n')
        file.write('hold : ' + str(self.get_hold_percentage(symbol, start_date, end_date)) + '%\n')
        file.close()
