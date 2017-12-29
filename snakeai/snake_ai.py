from abc import ABC, abstractmethod
from snakemodel.snake import Move


class SnakeAI(ABC):
    """Interface for an AI to play BattleSnake."""

    def __init__(self, game, heuristic):
        self.game = game
        self.heuristic = heuristic

    @abstractmethod
    def best_move(self):
        """Get the best move."""
        raise NotImplementedError("This methods need to be overrided.")

    def _get_candidate_moves(self, snake_id, board):
        """Get moves that will not lead to immediate death."""
        my_snake = board.snakes[snake_id]
        _, possible_head_cells = self._get_snake_next_possible_cells(
            self.game.you,
            board)
        candidate_moves = [move for move in Move]
        for move, head_cell in possible_head_cells.items():
            for other_snake_id in self.game.get_other_snake_ids(snake_id):
                other_body_cell, other_possible_heads = \
                    self._get_snake_next_possible_cells(
                        other_snake_id,
                        board)
                other_snake = board.snakes[other_snake_id]
                if head_cell in other_body_cell or (
                        (head_cell in other_possible_heads and
                         len(other_snake) >= len(my_snake))):
                    candidate_moves.remove(move)
                    break
        return candidate_moves

    def _get_snake_next_possible_cells(self, snake_id, board):
        """Get possible cells that a snake can occupy on the next turn."""
        snake = board.snakes[snake_id]
        next_body_cells = set(snake.body[:-1])
        possible_head_cells = {move: head_cell
                               for move, head_cell in
                               snake.get_possible_moves().items()
                               if head_cell in next_body_cells}
        return next_body_cells, possible_head_cells
