from models.n_tac_toe import NTacToe
import numpy as np

game = NTacToe([3,3], 3)

game.make_move((0,0))
game.print()
game.make_move((1,0))
game.print()