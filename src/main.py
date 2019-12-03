from managers.robinhood_manager import RobinhoodManager
from strategies.mean_reversion import MeanReversion
from datetime import datetime


def main():
    manager = RobinhoodManager()
    strategy = MeanReversion(90, 30)
    print(strategy.get_mock_percentage('TSLA', strategy.get_datetime_object('2019-01-01'), datetime.now()))
    print(strategy.get_hold_percentage('TSLA', strategy.get_datetime_object('2019-01-01'), datetime.now()))


main()
