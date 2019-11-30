from strategy import Strategy
from datetime import datetime

s = Strategy()
print(s.get_prices('TSLA', datetime.now(), datetime.now()))
