# from managers.robinhood_manager import RobinhoodManager
from strategies.mean_reversion import MeanReversion
from datetime import datetime


def main():
    # manager = RobinhoodManager()
    strategy = MeanReversion()
    strategy.do_best_intervals('VOO', strategy.get_datetime_object('2019-01-01'), datetime.now(), 'best_intervals/VOO')


main()
