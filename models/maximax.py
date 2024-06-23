import math
from typing import Dict, List

import numpy as np
from models.abstract_game import AbstractGame

def get_best_move(game: AbstractGame, depth: int = 6) -> object:
    best_move, _ = maximax(game, depth)
    return best_move

def maximax(game: AbstractGame, depth: int, cache:Dict={}) -> tuple[object, List[int]]:
    scale_factor = 0.95
    if game.is_game_over() or depth == 0:
        scores = (np.array(game.get_scores()) * scale_factor).tolist()
        return (None, scores)
    max_move: object
    max_relative_score: float = float('-inf')
    for move in game.get_legal_moves():
        new_game = game.clone()
        new_game.make_move(move)
        if new_game.__hash__() in cache:
            leaf_move, leaf_scores = cache[new_game.__hash__()]
        else:
            leaf_move, leaf_scores = maximax(new_game, depth-1, cache)
            cache[new_game.__hash__()] = (leaf_move, leaf_scores)
        
        leaf_relative_score = get_relative_score(leaf_scores, game.get_current_player())
        if leaf_relative_score > max_relative_score:
            max_move = move
            max_relative_score = leaf_relative_score
    return max_move, (np.array(leaf_scores) * scale_factor).tolist()

def get_relative_score(scores, player: int) -> float:
    if len(scores) == 1:
        return scores[0]
    other_ave = (sum(scores)-scores[player]) / (len(scores)-1)
    return scores[player] - other_ave
