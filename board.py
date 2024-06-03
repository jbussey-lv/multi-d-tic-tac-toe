from typing import List
import itertools
from itertools import product
import numpy as np

class Board:

  board = []
  win_length: int
  players: List[str]
  gravity_dimension: int
  
  def __init__(self,
               dimensions: List[int], 
               win_length: int,
               players = ['X', 'O'],
               gravity_dimension=None) -> None:
    self.board = np.full(dimensions, None)
    self.win_length = win_length
    self.players = players
    self.gravity_dimension = gravity_dimension
    
  def __str__(self) -> str:
    return str(self.board)
  
  def add_move(self, move: List[int], player: int) -> None:
    self.board[*move] = player

  def get_lines(self):
    dim_vals = [range(dim) for dim in self.board.shape]
    all_inds = np.array(list(product(*dim_vals)))
    start_inds = np.array([ind for ind in all_inds if 0 in ind])
    print(all_inds)
    print(start_inds)


  
  def check_line_win(self, line: List[int]) -> int|None:
    if len(line) < self.win_length:
      return False
    current_player = None
    tally = 0
    for val in line:
      if val is None:
        current_player = None
        tally = 0
      elif val == current_player:
        tally += 1
        if tally >= self.win_length:
          return current_player
      else:
        current_player = val
        tally = 1



board = Board([2,3,4], 4)

# board.add_move([1,2,3], 'X')
# board.add_move([2,3,4], 'Y')
# board.add_move([1,0,0], 'X')
print(board)
board.get_lines()

  