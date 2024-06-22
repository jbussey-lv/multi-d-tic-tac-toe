from abc import ABC, abstractmethod
from typing import List, Self

class AbstractGame(ABC):

    _players: List[str]

    def __init__(self, players: List[str]):
        self._players = players
        
    def get_players(self) -> List[str]:
        return self._players
    
    def __equal__(self, other: Self) -> bool:
        return self.__hash__() == other.__hash__()
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def get_legal_moves(self) -> List[object]:
        pass

    @abstractmethod
    def make_move(self, move: object) -> None:
        pass

    @abstractmethod
    def get_winner(self) -> str | None:
        pass

    @abstractmethod
    def get_scores(self) -> List[int]:
        pass

    @abstractmethod
    def clone(self) -> Self:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def get_current_player(self) -> int:
        pass
    
    def is_game_over(self) -> bool:
        return self.get_winner() is not None or len(self.get_legal_moves()) == 0


# def get_worst_score_sets(self) -> List[List[int]]:
#     return [self.get_worst_score_set_for_player(player) for player in range(len(self.players))]

#   def get_worst_score_set_for_player(self, player: int) -> List[int]:
#     worst_score_set = [math.inf] * len(self.players)
#     worst_score_set[player] = 0
#     return worst_score_set