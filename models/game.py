import math
from typing import Dict, List, Self, Tuple
import itertools
from itertools import product
import numpy as np

from models.clump import Clump

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
               gravity_dimension=None,
               lines: List[List[tuple[int]]]|None = None) -> None:
    self.board = np.full(shape, None)
    self.win_length = win_length
    self.players = players
    self.gravity_dimension = gravity_dimension
    self.lines = build_all_lines(shape, win_length) if lines is None else lines

  def add_move_interactive(self, move: tuple[int]) -> None:
    if not self.is_move_legal(move):
      print("Move is not legal")
      return
    self.add_move(move)
    print(self)
    if self.is_over():
      print("Game over")
      return
    print(self.players[self.whose_turn()], "to move")
    move = self.get_best_move()
    self.add_move(move)
    print(self)
    if self.is_over():
      print("Game over")
      return
    print(self.players[self.whose_turn()], "to move")

  def copy(self) -> Self:
    game = Game(
      self.board.shape,
      self.win_length,
      self.players,
      self.gravity_dimension,
      self.lines)
    game.board = self.board.copy()
    return game
  
  def get_best_move(self, depth: int = 7) -> List[int]:
    worst_relative_scores = [0]*len(self.players)
    best_move_index, score_set = self.minimax(depth, worst_relative_scores)
    legal_moves = self.get_legal_moves()
    best_move = legal_moves[best_move_index]
    return best_move
  
  def get_worst_score_sets(self) -> List[List[int]]:
    return [self.get_worst_score_set_for_player(player) for player in range(len(self.players))]

  def get_worst_score_set_for_player(self, player: int) -> List[int]:
    worst_score_set = [math.inf] * len(self.players)
    worst_score_set[player] = 0
    return worst_score_set

  def minimax(self, depth: int, worst_relative_scores: List[int]) -> Tuple[int, List[int]]:

    DISCOUNT_FACTOR = 0.9

    if self.is_over() or depth == 0:
      return (0, self.get_score_set())

    best_relative_score = 0
    best_move_index = 0

    worst_relative_score = worst_relative_scores[self.whose_turn()]
    prev_player_worst_relative_score = worst_relative_scores[self.whose_turn_pervious()]
    
    for move_index, next_game in enumerate(self.get_next_games()):
      score_set_index, next_game_score_set = next_game.minimax(depth - 1)
      next_game_relative_score = get_relative_score(next_game_score_set, self.whose_turn())

      if next_game_relative_score > best_relative_score:
        best_relative_score = next_game_relative_score
        best_move_index = move_index

      worst_relative_score = min(worst_relative_score, next_game_relative_score)
      if worst_relative_score <= best_relative_score:
        break

      preferred_index, best_option = get_preferred_score_set(
        [best_option, next_game_score_set], self.whose_turn())
      
      worst_relative_scores[self.whose_turn()] = best_option

    score_sets = [score_set for index, score_set in indexed_score_sets]
    preferred_score_set = get_preferred_score_set(score_sets, self.whose_turn())
    discounted_preferred_score_set = [score * DISCOUNT_FACTOR for score in preferred_score_set[1]]

    return discounted_preferred_score_set
  
  def is_over(self):
    if self.get_winner() is not None:
      return True
    if self.get_legal_moves() == []:
      return True
    return False

  def get_winner(self) -> int|None:
    run_sets = self.get_run_sets()
    for player_num, run_set in enumerate(run_sets):
      for run_length, count in run_set.items():
        if count > 0 and run_length >= self.win_length:
          return player_num
    return None
  
  def get_next_games(self) -> List[Self]:
    next_games = []
    for move in self.get_legal_moves():
      next_games.append(self.copy_with_move(move))
    return next_games

  def copy_with_move(self, move: tuple[int]) -> Self:
    game = self.copy()
    game.add_move(move)
    return game

  def get_legal_moves(self) -> List[tuple[int]]:
    legal_moves_np = np.argwhere(self.board == None)
    return list(map(tuple, legal_moves_np))
  
  def is_move_legal(self, move: tuple[int]) -> bool:
    if len(self.board.shape) != len(move):
      return False
    if self.is_over():
      return False
    return self.board[*move] == None
  
  def get_move_count(self) -> int:
    return (self.board != None).sum()
  
  def whose_turn(self) -> int:
    return self.get_move_count() % len(self.players)
  
  def whose_turn_pervious(self) -> int:
    return (self.get_move_count() - 1) % len(self.players)
    
  def __str__(self) -> None:
    c = np.copy(self.board)
    c[c == None] = '.'
    for i, player in enumerate(self.players):
      c[c == i] = player
    return np.array2string(c, separator=' ', formatter={'all': lambda c: c})
  
  def run_set_to_score(self, run_set):
    score = 0
    for run_length, tally in run_set.items():
      score += tally * (run_length ** run_length)
    return score

  def get_score_set(self) -> List[int]:
    runs = self.get_run_sets()
    score_set = [self.run_set_to_score(run) for run in runs]
    winner = self.get_winner()
    if winner is not None:
      for player in range(len(score_set)):
        if player != winner:
          score_set[player] = 0
    return score_set
  
  
  def add_move(self, move: tuple[int]) -> None:
    player = self.whose_turn()
    if not self.is_move_legal(move):
      raise ValueError("Move is not legal")
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




# get lengths of sequences plus padding on Nones   
def get_runs_from_sequence(sequence: List, win_length: int, num_players: int) -> Dict[int, List]:

  runs = get_empty_run_sets(win_length, num_players)

  clumps = get_clumps(sequence)

  for clump in clumps:
    if clump.get_total_length() >= win_length:
      run_length = min([clump.run_length, win_length])
      runs[clump.player][run_length] += 1

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


def get_empty_run_sets(win_length: int, num_players: int) -> Dict[int, List]:
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

  
def get_relative_score(score_set: List[int], player: int) -> int:
  avg_without_player = (sum(score_set) - score_set[player]) / (len(score_set) - 1)
  return score_set[player] - avg_without_player

def get_preferred_score_set(score_sets: List[List[int]], player: int) -> Tuple[int, List[int]]:
  relative_scores = [get_relative_score(score_set, player) for score_set in score_sets]
  max_relative_score = max(relative_scores)
  max_index = relative_scores.index(max_relative_score)
  return max_index, score_sets[max_index]


