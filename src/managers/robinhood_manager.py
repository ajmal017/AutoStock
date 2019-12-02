from manager import Manager
from shell.shell import RobinhoodShell


class RobinhoodManager(Manager):

    robinhood_shell = RobinhoodShell()

    def buy(self, symbol, shares_count):
        instrument = self.robinhood_shell.get_instrument(symbol)
        self.robinhood_shell.trader.place_buy_order(instrument, shares_count)

    def sell(self, symbol, shares_count):
        instrument = self.robinhood_shell.get_instrument(symbol)
        self.robinhood_shell.trader.place_sell_order(instrument, shares_count)
