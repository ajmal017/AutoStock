from managers.robinhood_manager import RobinhoodManager
from strategies.mean_reversion import MeanReversion
from datetime import datetime


def main():
    manager = RobinhoodManager()
    strategy = MeanReversion(26, 2)
    # print(strategy.get_mock_percentage('ACB', strategy.get_datetime_object('2019-01-01'), datetime.now()))
    # print(strategy.get_hold_percentage('ACB', strategy.get_datetime_object('2019-01-01'), datetime.now()))
    print(strategy.get_best_intervals('VOO', strategy.get_datetime_object('2015-01-01'), datetime.now()))

main()
