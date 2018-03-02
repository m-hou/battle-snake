import unittest
from snakemodel.game import Game
from snakemodel.snake import Move
from snakeai.snake_ai import SnakeAI
from snakeai.heuristic import Heuristic
from test_util import load_game


class TestSnakeAI(unittest.TestCase):
    """Tests for SnakeAI logic."""

    def test_diagonal_head(self):
        """Test scenario where a larger snake is diagonally adjacent."""
        curr_game = load_game('test_cases/diagonal_head2.json')
        heuristic = Heuristic()
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertEqual(
            set(snake_ai.get_candidate_moves(curr_game.you, curr_game.board)),
            set([Move.LEFT, Move.DOWN]))

    def test_best_move(self):
        """Test scenario where a larger snake is diagonally adjacent."""
        curr_game = load_game('test_cases/a.json')
        heuristic = Heuristic(1)
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertEqual(snake_ai.best_move(), Move.LEFT.get_move())
