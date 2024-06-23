from models.abstract_game import AbstractGame
from models.n_tac_toe import NTacToe
from models.maximax import get_best_move, maximax

n_tac_toe = NTacToe((4,4), 3)

print(n_tac_toe)

while not n_tac_toe.is_game_over():
  print(n_tac_toe.get_players()[n_tac_toe.get_current_player()], "to move")
  move = input("Enter move: ")
  n_tac_toe.make_move(eval(move))

  print(n_tac_toe)
  if n_tac_toe.is_game_over():
    winner = n_tac_toe.get_winner()
    if winner is not None:
      print(n_tac_toe.get_players()[winner], "wins!")
    else:
      print("It's a draw!")
    break

  print(n_tac_toe.get_players()[n_tac_toe.get_current_player()], "to move")
  ai_move = get_best_move(n_tac_toe)
  n_tac_toe.make_move(ai_move)
  print(n_tac_toe)
  if n_tac_toe.is_game_over():
    winner = n_tac_toe.get_winner()
    if winner is not None:
      print(n_tac_toe.get_players()[winner], "wins!")
    else:
      print("It's a draw!")
    break
# def add_move_interactive(self, game: AbstractGame, player_move: object) -> None:
    
#     try:
#       game.make_move(player_move)
#     except:
#       print("Move is not legal")
#       return
#     print(self)
#     if game.is_game_over():
#       print("Game over")
#       return
#     print(game.get_players()[game.get_current_player()], "to move")
    
#     ai_move = get_best_move(game,5)
#     game.make_move(ai_move)
#     print(self)
#     if game.is_game_over():
#       print("Game over")
#       return
#     print(game.get_players()[game.get_current_player()], "to move")