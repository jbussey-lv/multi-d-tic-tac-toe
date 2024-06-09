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
    lines = []
    dim_vals_full = [list(range(dim)) for dim in self.board.shape]
    for zero_dim in range(self.board.ndim):
      dim_vals = dim_vals_full.copy()
      dim_vals[zero_dim] = [0]
      all_inds = np.array(list(product(*dim_vals)))
      for ind in all_inds:
        line = [ind]
        for i in range(1, self.board.shape[zero_dim]):
          new_ind = ind.copy()
          new_ind[zero_dim] += i
          line.append(new_ind)
        lines.append(line)
    return np.array(lines)


  
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



# board = Board([2,3,4], 4)

# # board.add_move([1,2,3], 'X')
# # board.add_move([2,3,4], 'Y')
# # board.add_move([1,0,0], 'X')
# print(board)
# lines = board.get_lines()
# print(len(lines))
# print(lines)

def middle_out(start: tuple[int], diff: tuple[int], shape: tuple[int]) -> bool:
  for i, val in enumerate(start):
    if val in [0, shape[i] - 1] and diff[i] != 0:
      return False
  return True

def build_all_lines(shape: tuple[int], win_length: int):
  lines = []
  starts = get_start_points(shape)
  diffs = get_diffs(shape)
  for start in starts:
    for diff in diffs:
      if middle_out(start, diff, shape):
        continue
      line = build_line(shape, start, diff)
      if len(line) >= win_length and line not in lines:
        lines.append(line)
  return sorted(lines)

def get_start_points(shape: tuple[int]) -> List[tuple[int]]:
  dim_vals = [range(dim) for dim in shape]
  all_points = product(*dim_vals)
  start_points: List[tuple[int]] = [tuple(point) for point in all_points if is_start(tuple(point), shape)]
  return start_points

def is_start(point: tuple[int], shape: tuple[int]):
  for i, val in enumerate(point):
    if val == 0 or val == shape[i] - 1:
      return True
  return False

def build_line(shape: tuple[int], start: tuple[int], diffs: tuple[int]):
  shape = np.array(shape)
  point = np.array(start)
  line = []
  # while the point is within the bounds of the shape
  while (point >= 0).all() and (point < shape).all():
    line.append(tuple(point))
    point = np.array(np.add(point, diffs))
  return sorted(line)
  
  
def get_diffs(shape: tuple[int]) -> tuple[tuple[int]]:
  all_diffs = product(*[(-1,0,1)]*len(shape))
  full_zero = (0,)*len(shape)
  return tuple([diff for diff in all_diffs if diff != full_zero])
