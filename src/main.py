from managers.robinhood_manager import RobinhoodManager
from strategies.my_random import MyRandom


def main():
    manager = RobinhoodManager()
    strategy = MyRandom()
    manager.do_move('TSLA', 1, strategy)


main()
