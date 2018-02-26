from copy import deepcopy
from .board import Board


class Game:
    """The game."""

    def __init__(self, data):
        self.board = Board(data)
        self.game_id = data['game_id'] if 'game_id' in data else 0
        self.turn = data['turn']
        self.you = data['you']['id']
        self.snake_ids = self._get_snake_ids(data)

    def simulate_moves(self, board, snake_id_move_mapping):
        """Simulate the outcome of applying moves to a board"""
        return deepcopy(board).update_board(snake_id_move_mapping)

    def _get_snake_ids(self, data):
        """Get the ids of all the players"""
        return [snake['id'] for snake in data['snakes']['data']]

    def get_other_snake_ids(self, self_snake_id):
        """Return ids of other players"""
        return [snake_id
                for snake_id in self.snake_ids
                if snake_id != self_snake_id]
