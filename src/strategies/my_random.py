from strategy import Strategy
from move import Move
from random import choice


class MyRandom(Strategy):
    days_back_length = 0

    def get_move(self, prices, last_move, index=-1):
        moves = [Move.BUY, Move.SELL, Move.HOLD]
        return choice(moves)
