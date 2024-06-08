from models import board

def test_get_start_points_flat():
   returned = board.get_start_points((3,3))
   correct = [(0,0), (0,1), (0,2), 
              (1,0),        (1,2),
              (2,0), (2,1), (2,2)]
   assert returned == correct

def test_get_start_points_3d():
   returned = board.get_start_points((3,4,3))
   correct = [(0,0,0), (0,0,1), (0,0,2), 
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
              ]
   assert returned == correct