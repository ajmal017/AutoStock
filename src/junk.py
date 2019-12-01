from strategy import Strategy
from strategies import my_random
from datetime import datetime
from move import Move

s = my_random.MyRandom()
print(s.get_mock_percentage('AAPL', s.get_datetime_object('2019-01-01'), datetime.now()))
print(s.get_hold_percentage('AAPL', s.get_datetime_object('2019-01-01'), datetime.now()))
