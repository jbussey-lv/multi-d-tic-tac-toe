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