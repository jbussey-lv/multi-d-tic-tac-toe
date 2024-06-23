import math
from typing import Dict, List, Self, Tuple
import itertools
from itertools import product
import numpy as np

from models.abstract_game import AbstractGame
from models.clump import Clump

class NTacToe(AbstractGame):

  board: np.ndarray
  win_length: int
  gravity_dimension: int|None
  lines: List[List[tuple[int]]]
  
  def __init__(self,
               shape: Tuple[int, ...], 
               win_length: int,
               players = ['X', 'O'],
               gravity_dimension=None,
               lines: List[List[tuple[int]]]|None = None) -> None:
    self.board = np.full(shape, None)
    self.win_length = win_length
    self.players = players
    self.gravity_dimension = gravity_dimension
    self.lines = build_all_lines(shape, win_length) if lines is None else lines

    super().__init__(players)

  def __hash__(self) -> int:
    return hash(str(self.board))
  
  def __repr__(self) -> str:
    return self.board.__repr__()

  def clone(self) -> "NTacToe":
    game = NTacToe(
      self.board.shape,
      self.win_length,
      self.players,
      self.gravity_dimension,
      self.lines)
    game.board = self.board.copy()
    return game


  def get_winner(self) -> int|None:
    run_sets = self.get_run_sets()
    for player_num, run_set in enumerate(run_sets):
      for run_length, count in run_set.items():
        if count > 0 and run_length >= self.win_length:
          return player_num
    return None    

  def get_legal_moves(self) -> List[tuple[int]]:
    if self.get_winner() is not None:
      return []
    open_spaces_np = np.argwhere(self.board == None)
    return list(map(tuple, open_spaces_np))
  
  def get_move_count(self) -> int:
    return (self.board != None).sum()
  
  def get_current_player(self) -> int:
    return self.get_move_count() % len(self.players)
  
  def whose_turn_pervious(self) -> int:
    return (self.get_move_count() - 1) % len(self.players)
    
  # def __str__(self) -> str:
  #   c = np.copy(self.board)
  #   c[c == None] = '.'
  #   for i, player in enumerate(self.players):
  #     c[c == i] = player
  #   return np.array2string(c, separator=' ', formatter={'all': lambda c: c})
  
  def run_set_to_score(self, run_set):
    score = 0
    for run_length, tally in run_set.items():
      score += tally * (run_length ** run_length)
    return score

  def get_scores(self) -> List[int]:
    runs = self.get_run_sets()
    scores = [self.run_set_to_score(run) for run in runs]
    winner = self.get_winner()
    if winner is not None:
      for player in range(len(scores)):
        if player != winner:
          scores[player] = 0
    return scores
  
  def make_move(self, move: tuple[int, ...]) -> None:
    if move not in self.get_legal_moves():
      raise ValueError("Move is not legal")
    
    player = self.get_current_player()
    
    self.board[*move] = player
      
    
  def get_run_sets(self) -> List[Dict[int, int]]:
    run_sets = get_empty_run_sets(self.win_length, len(self.players))
    
    for sequence in self.get_sequences():
      sequence_runs = get_runs_from_sequence(sequence, self.win_length, len(self.players))
      for player, run in enumerate(sequence_runs):
        for run_length, tally in run.items():
          run_sets[player][run_length] += tally

    return run_sets

  def get_sequences(self) -> List:
    return [self.line_to_sequence(line) for line in self.lines]

  def line_to_sequence(self,line):
    return [self.board[*point] for point in line]


def is_all_none(sequence: List) -> bool:
  return all([val is None for val in sequence])

# get lengths of sequences plus padding on Nones   
def get_runs_from_sequence(sequence: List, win_length: int, num_players: int) -> List[Dict[int, int]]:

  runs = get_empty_run_sets(win_length, num_players)

  if is_all_none(sequence):
    return runs
  
  for i in range(0, len(sequence)-win_length+1):
    tail_i = i-1
    head_i = i+win_length
    chunk = sequence[i:i+win_length]
    if is_all_none(chunk):
      continue

    denoned_chunk = [val for val in chunk if val is not None]

    denoned_set = set(denoned_chunk)
    if len(denoned_set) == 1:
      player = denoned_set.pop()
      run_length = len(denoned_chunk)
      if tail_i >= 0 and sequence[tail_i] == player:
        continue
      if head_i < len(sequence) and sequence[head_i] == player:
        continue
      runs[player][run_length] += 1

  return runs


def get_clumps(sequence: List) -> List[Clump]:
  start_pos = 0
  clumps = []
  go = True

  while start_pos < len(sequence) and go:
    clump = Clump()
    right_sequence = sequence[start_pos:]
    for i, player in enumerate(right_sequence):
      if i == len(right_sequence)-1:
        go = False
      if clump.status == "head":
        if player is not None:
          clump.player = player
          clump.run_length += 1
          clump.status = "run"
        else:
          clump.head_length += 1
      elif clump.status == "run":
        if player == clump.player:
          clump.run_length += 1
        elif player is None:
          clump.status = "tail"
          clump.tail_length += 1
        else:
          clumps.append(clump)
          start_pos = start_pos + clump.get_claimed_length()
          break
      elif clump.status == "tail":
        if player is None:
          clump.tail_length += 1
        else:
          clumps.append(clump)
          start_pos = start_pos + clump.get_claimed_length()
          break
      if go == False and clump.player is not None:
        clumps.append(clump)
  return clumps


def get_empty_run_sets(win_length: int, num_players: int) -> List[Dict[int, int]]:
  runs: List[Dict[int, int]] = [{} for _ in range(num_players)]
  for player_num in range(num_players):
    run = {}
    for run_length in range(1, win_length + 1):
      run[run_length] = 0
    runs[player_num] = run
  return runs
    

def is_middle_out(start: tuple[int, ...], diff: tuple[int, ...], shape: tuple[int, ...]) -> bool:
  for i, val in enumerate(start):
    if val in [0, shape[i] - 1] and diff[i] != 0:
      return False
  return True

def build_all_lines(shape: tuple[int, ...], win_length: int):
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

def get_start_points(shape: tuple[int, ...]) -> List[tuple[int, ...]]:
  dim_vals = [range(dim) for dim in shape]
  all_points = product(*dim_vals)
  start_points = [tuple(point) for point in all_points if is_start(tuple(point), shape)]
  return start_points

def is_start(point: tuple[int, ...], shape: tuple[int, ...]):
  for i, val in enumerate(point):
    if val == 0 or val == shape[i] - 1:
      return True
  return False

def build_line(shape: Tuple[int, ...], start: tuple[int, ...], diffs: tuple[int, ...]):
  point = np.array(start)
  line = []
  # while the point is within the bounds of the shape
  while (point >= 0).all() and (point < shape).all():
    line.append(tuple(point))
    point = np.array(np.add(point, diffs))
  return sorted(line)
  
  
def get_diffs(shape: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
  all_diffs = product(*[(-1,0,1)]*len(shape))
  full_zero = (0,)*len(shape)
  return tuple([diff for diff in all_diffs if diff != full_zero])




