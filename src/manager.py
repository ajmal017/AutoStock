from move import Move


class Manager:

    def buy(self, symbol, shares_count):
        pass

    def sell(self, symbol, shares_count):
        pass

    def do_move(self, symbol, shares_count, strategy):
        move = strategy.get_current_move(symbol)
        if move == Move.BUY:
            self.buy(symbol, shares_count)
            print('bought {shares_count} shares of {symbol}'.format(shares_count=shares_count, symbol=symbol))
        elif move == Move.SELL:
            self.sell(symbol, shares_count)
            print('sold {shares_count} shares of {symbol}'.format(shares_count=shares_count, symbol=symbol))
        elif move == Move.HOLD:
            print('held {symbol}'.format(symbol=symbol))
        elif not move:
            print('market is closed')
