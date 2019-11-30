from strategy import Strategy
from strategies import my_random
from datetime import datetime
from move import Move

s = my_random.MyRandom()
print(s.get_mock_percentage('TSLA', s.get_datetime_object('2019-01-01'), datetime.now()))
