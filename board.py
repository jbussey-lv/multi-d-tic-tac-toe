from typing import List
import itertools
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

  def iterate_lines(self):
    for axis in range(len(self.board.shape)):
      for line in self.board:
        yield line
      for line in self.board.T:
        yield line
      for line in itertools.chain(
        [self.board.diagonal(i) for i in range(-self.board.shape[0]+1, self.board.shape[1])],
        [self.board[:, ::-1].diagonal(i) for i in range(-self.board.shape[0]+1, self.board.shape[1])]):
        yield line
  
  def add_move(self, move: List[int], player: int) -> None:
    self.board[*move] = player
  
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



board = Board([3,4,5], 4)

board.add_move([1,2,3], 'X')
board.add_move([2,3,4], 'Y')
board.add_move([1,0,0], 'X')

print(board)
for line in board.iterate_lines():
  print(line)

  