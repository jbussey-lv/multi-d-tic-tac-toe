from models.game import Game
import numpy as np

game = Game([3,3], 3)

game.add_move((0,0))
game.print()
game.add_move((1,0))
game.print()