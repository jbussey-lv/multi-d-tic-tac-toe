from typing import Dict, List
import itertools
from itertools import product
import numpy as np

class Game:

  board = []
  win_length: int
  players: List[str]
  gravity_dimension: int
  lines: List[List[tuple[int]]]
  
  def __init__(self,
               shape: List[int], 
               win_length: int,
               players = ['X', 'O'],
               gravity_dimension=None) -> None:
    self.board = np.full(shape, None)
    self.win_length = win_length
    self.players = players
    self.gravity_dimension = gravity_dimension
    self.lines = build_all_lines(shape, win_length)
    
  def __str__(self) -> str:
    return str(self.board)
  
  def add_move(self, move: List[int], player: int) -> None:
    self.board[*move] = player




# board = Board([2,3,4], 4)

# # board.add_move([1,2,3], 'X')
# # board.add_move([2,3,4], 'Y')
# # board.add_move([1,0,0], 'X')
# print(board)
# lines = board.get_lines()
# print(len(lines))
# print(lines)

# get lengths of sequences plus padding on Nones   
def get_runs_from_sequence(sequence: List, win_length: int, num_players: int) -> Dict[int, List]:

  runs = get_empty_runs(win_length, num_players)

  clumps = get_clumps(sequence)

  for clump in clumps:
    if clump["head_length"] + clump["run_length"] + clump["tail_length"] >= win_length:
      runs[clump['active_player']][clump["run_length"]] += 1

  return runs


def get_clumps(sequence: List):
  start_pos = 0
  clumps = []
  go = True

  while start_pos < len(sequence) and go:
    status = 'head'
    clump = {
      'active_player': None,
      'head_length': 0,
      'run_length': 0,
      'tail_length': 0
    }
    right_sequence = sequence[start_pos:]
    for i, player in enumerate(right_sequence):
      if i == len(right_sequence)-1:
        go = False
      if status == "head":
        if player is not None:
          clump['active_player'] = player
          clump['run_length'] += 1
          status = "run"
        else:
          clump['head_length'] += 1
      elif status == "run":
        if player == clump['active_player']:
          clump['run_length'] += 1
        elif player is None:
          status = "tail"
          clump['tail_length'] += 1
        else:
          clumps.append(clump)
          start_pos = start_pos + clump['head_length'] + clump['run_length']
          break
      elif status == "tail":
        if player is None:
          clump['tail_length'] += 1
        else:
          clumps.append(clump)
          start_pos = start_pos + clump['head_length'] + clump['run_length']
          break
      if go == False:
        clumps.append(clump)
  return clumps

    
  clumps = get_empty_runs(win_length, num_players)
  count = 0
  active_player = None
  for i in range(len(sequence)):
    curr_spot = sequence[i]
    prev_spot = sequence[i-1] if i > 0 else None
    if curr_spot is None:
      pass
    elif curr_spot == active_player:
      pass
    else:
      pass



def get_empty_runs(win_length: int, num_players: int) -> Dict[int, List]:
  runs = [None] * num_players
  for player_num in range(num_players):
    run = {}
    for run_length in range(1, win_length + 1):
      run[run_length] = 0
    runs[player_num] = run
  return runs
    

def is_middle_out(start: tuple[int], diff: tuple[int], shape: tuple[int]) -> bool:
  for i, val in enumerate(start):
    if val in [0, shape[i] - 1] and diff[i] != 0:
      return False
  return True

def build_all_lines(shape: tuple[int], win_length: int):
  lines = []
  starts = get_start_points(shape)
  diffs = get_diffs(shape)
  for(start, diff) in itertools.product(starts, diffs):
    if is_middle_out(start, diff, shape):
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
