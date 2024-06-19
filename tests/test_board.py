import pytest
from models import game

get_start_point_inputs = [
   ((3,3), [(0,0), (0,1), (0,2), 
            (1,0),        (1,2),
            (2,0), (2,1), (2,2)]),
   ((3,4,3), [(0,0,0), (0,0,1), (0,0,2), 
              (0,1,0), (0,1,1), (0,1,2),
              (0,2,0), (0,2,1), (0,2,2),
              (0,3,0), (0,3,1), (0,3,2),
              
              (1,0,0), (1,0,1), (1,0,2), 
              (1,1,0),          (1,1,2),
              (1,2,0),          (1,2,2),
              (1,3,0), (1,3,1), (1,3,2),
              
              (2,0,0), (2,0,1), (2,0,2), 
              (2,1,0), (2,1,1), (2,1,2),
              (2,2,0), (2,2,1), (2,2,2),
              (2,3,0), (2,3,1), (2,3,2)
              ]),
]
@pytest.mark.parametrize("shape,expected", get_start_point_inputs)
def test_get_start_points(shape, expected):
   returned = game.get_start_points(shape)
   assert returned == expected

build_line_inputs = [   
   ((3,3), (0,0), (0,1), [(0,0), (0,1), (0,2)]),   
   ((3,3), (0,0), (1,1), [(0,0), (1,1), (2,2)]),   
   ((3,3,4), (2,2,3), (-1,-1,-1), [(0,0,1), (1,1,2), (2,2,3)]),         
]
@pytest.mark.parametrize("shape,start,diffs,expected", build_line_inputs)
def test_build_line(shape, start, diffs, expected):
   returned = game.build_line(shape, start, diffs)
   assert returned == expected

build_all_lines_output_inputs = [ 
   ((2,2,2), 2, [    
      [(0, 0, 0), (0, 0, 1)], 
      [(0, 0, 0), (0, 1, 0)], 
      [(0, 0, 0), (0, 1, 1)], 
      [(0, 0, 0), (1, 0, 0)],
      [(0, 0, 0), (1, 0, 1)],
      [(0, 0, 0), (1, 1, 0)],
      [(0, 0, 0), (1, 1, 1)],
      [(0, 0, 1), (0, 1, 0)],
      [(0, 0, 1), (0, 1, 1)],
      [(0, 0, 1), (1, 0, 0)],
      [(0, 0, 1), (1, 0, 1)],
      [(0, 0, 1), (1, 1, 0)],
      [(0, 0, 1), (1, 1, 1)],
      [(0, 1, 0), (0, 1, 1)],
      [(0, 1, 0), (1, 0, 0)],
      [(0, 1, 0), (1, 0, 1)],
      [(0, 1, 0), (1, 1, 0)],
      [(0, 1, 0), (1, 1, 1)],
      [(0, 1, 1), (1, 0, 0)],
      [(0, 1, 1), (1, 0, 1)],
      [(0, 1, 1), (1, 1, 0)],
      [(0, 1, 1), (1, 1, 1)],
      [(1, 0, 0), (1, 0, 1)],
      [(1, 0, 0), (1, 1, 0)],
      [(1, 0, 0), (1, 1, 1)],
      [(1, 0, 1), (1, 1, 0)],
      [(1, 0, 1), (1, 1, 1)],
      [(1, 1, 0), (1, 1, 1)]
   ]),
   ((3,3), 3, [
      [(0,0), (0,1), (0,2)],
      [(0,0), (1,0), (2,0)],
      [(0,0), (1,1), (2,2)],
      [(0,1), (1,1), (2,1)],
      [(0,2), (1,1), (2,0)],
      [(0,2), (1,2), (2,2)],
      [(1,0), (1,1), (1,2)],
      [(2,0), (2,1), (2,2)],
   ]),
   ((3,2), 2, [
      [(0,0), (0,1)],
      [(0,0), (1,0), (2,0)],
      [(0,0), (1,1)],
      [(0,1), (1,0)],
      [(0,1), (1,1), (2,1)],
      [(1,0), (1,1)],
      [(1,0), (2,1)],
      [(1,1), (2,0)],
      [(2,0), (2,1)],
   ])
]
@pytest.mark.parametrize("shape,win_length,expected", build_all_lines_output_inputs)
def test_build_all_lines_output(shape, win_length, expected):
   returned = game.build_all_lines(shape, win_length)
   assert returned == expected

build_all_lines_len_inputs = [
   ((2,2,2), 2, 28),
   ((3,3), 3, 8),
   ((3,2), 2, 9),
   ((4,4,4), 4, 76),
   ((4,4,3), 3, 106),
]
@pytest.mark.parametrize("shape,win_length,expected", build_all_lines_len_inputs)
def test_build_all_lines_len(shape, win_length, expected):
   returned = game.build_all_lines(shape, win_length)
   assert len(returned) == expected

def test_get_runs_from_sequence():
   actual = game.get_runs_from_sequence([None, 1, 1, None, 0, 0, 0, 1, 1], 3, 2)
   expected = [{1: 0, 2: 0, 3: 1}, {1: 0, 2: 1, 3: 0}]
   assert actual == expected
   
def test_get_empty_runs():
   empty_run = game.get_empty_run_sets(3, 2)
   assert empty_run == [{1: 0, 2: 0, 3: 0}, {1: 0, 2: 0, 3: 0}]

def test_get_runs():
   g = game.Game([3,3], 3)
   g.add_move((0,0))
   g.add_move((1,2))
   g.add_move((0,1))
   actual = g.get_run_sets()
   expected = [{1: 3, 2: 1, 3: 0}, {1: 2, 2: 0, 3: 0}]
   assert actual == expected

def test_get_score_set():
   g = game.Game([3,3], 3)
   g.add_move((0,0))
   g.add_move((1,2))
   g.add_move((0,1))
   actual = g.get_score_set()
   expected = [7, 2]
   assert actual == expected

def test_whose_turn():
   g = game.Game([3,3], 3, ['x', 'y', 'z'])
   g.add_move((0,0))
   g.add_move((1,2))
   g.add_move((0,1))
   assert g.whose_turn() == 0

get_relative_scores_inputs = [
   ([1,2,3], 0, -1.5),
   ((1,2,3), 2, 1.5),
   ((1,2,3), 1, 0),
   ((4,4,4), 0, 0),
   ((9,2), 0, 7),
]
@pytest.mark.parametrize("score_set,player,expected", get_relative_scores_inputs)
def test_get_relative_score(score_set, player, expected):
   score_set = [1, 2, 3]
   player = 0
   expected = -1.5
   actual = game.get_relative_score(score_set, player)
   assert actual == expected

def test_get_preferred_score_set():
   score_sets = [
      [1, 2, 3],
      [2, 1, 3],
      [3, 2, 1],
   ]
   player = 0
   expected = (2, [3,2,1])
   actual = game.get_preferred_score_set(score_sets, player)
   assert actual == expected

def test_get_best_move():
   g = game.Game([3,3], 3)
   g.add_move((0,1))
   actual = g.get_best_move(5)
   expected = (0,2)
   assert actual == expected