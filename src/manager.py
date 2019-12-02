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
        elif move == Move.SELL:
            self.sell(symbol, shares_count)
