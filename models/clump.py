

class Clump():

  status = "head"
  player = None
  head_length = 0
  run_length = 0
  tail_length = 0

  def get_total_length(self):
    return self.head_length + self.run_length + self.tail_length
  
  def get_claimed_length(self):
    return self.head_length + self.run_length