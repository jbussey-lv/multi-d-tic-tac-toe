import pytest
from models import board

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
def test_get_start_points_flat(shape, expected):
   returned = board.get_start_points(shape)
   assert returned == expected

build_line_inputs = [   
   ((3,3), (0,0), (0,1), [(0,0), (0,1), (0,2)]),   
   ((3,3), (0,0), (1,1), [(0,0), (1,1), (2,2)]),   
   ((3,3,4), (2,2,3), (-1,-1,-1), [(0,0,1), (1,1,2), (2,2,3)]),         
]
@pytest.mark.parametrize("shape,start,diffs,expected", build_line_inputs)
def test_build_line(shape, start, diffs, expected):
   returned = board.build_line(shape, start, diffs)
   assert returned == expected

def test_build_all_lines_2d():
   returned = board.build_all_lines((3,3), 3)
   correct = [
      [(0,0), (0,1), (0,2)],
      [(0,0), (1,0), (2,0)],
      [(0,0), (1,1), (2,2)],
      [(0,1), (1,1), (2,1)],
      [(0,2), (1,1), (2,0)],
      [(0,2), (1,2), (2,2)],
      [(1,0), (1,1), (1,2)],
      [(2,0), (2,1), (2,2)],
   ]
   assert returned == correct