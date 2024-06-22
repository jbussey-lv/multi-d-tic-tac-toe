import math
from typing import Dict, List
from models.abstract_game import AbstractGame

def get_best_move(game: AbstractGame, depth: int = 5) -> object:
    _, best_move, _ = maximax(game, depth)
    return best_move

def maximax(game: AbstractGame, depth: int, cache:Dict[AbstractGame,tuple[int, object, AbstractGame]]={}) -> tuple[int, object, AbstractGame]:
    scale_factor = 0.9
    if game.is_game_over() or depth == 0:
        return (depth, None, game)
    max_relative_score = -math.inf
    max_depth: int
    max_move: object
    max_game: AbstractGame
    for move in enumerate(game.get_legal_moves()):
        new_game = game.clone()
        new_game.make_move(move)
        if new_game in cache:
            leaf_depth, _, leaf_game = cache[new_game]
        else:
            leaf_depth, _, leaf_game = maximax(new_game, depth-1)
            cache[new_game] = (leaf_depth, None, leaf_game)

        depth_diff = depth - leaf_depth
        relative_score = get_relative_score(leaf_game, game.get_current_player())
        scaled_relative_score = relative_score * scale_factor ** depth_diff
        if scaled_relative_score > max_relative_score:
            max_relative_score = scaled_relative_score
            max_depth = leaf_depth
            max_move = move
            max_game = leaf_game
    return max_depth, max_move, max_game

def get_relative_score(game: AbstractGame, player: int) -> float:
    scores = game.get_scores()
    if len(scores) == 1:
        return scores[0]
    other_ave = (sum(scores)-scores[player]) / (len(scores)-1)
    return scores[player] - other_ave
