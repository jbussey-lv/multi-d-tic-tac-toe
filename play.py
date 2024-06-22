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