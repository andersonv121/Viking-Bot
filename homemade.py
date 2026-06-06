import chess
from chess.engine import PlayResult
from lib.engine_wrapper import MinimalEngine
from engine import get_best_move
import time

class ExampleEngine(MinimalEngine):
    pass

class MyEngine(MinimalEngine):

    def search(self, board: chess.Board, *args):
        move = get_best_move(board)
        return PlayResult(move, None)
    
ENGINE_CLASS = MyEngine
