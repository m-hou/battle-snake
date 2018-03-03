import unittest
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

    def test_food_trap(self):
        """Test scenario where adjacent food is a trap."""
        curr_game = load_game('test_cases/next_to_food_trap.json')
        heuristic = Heuristic()
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertEqual(
            set(snake_ai.get_candidate_moves(curr_game.you, curr_game.board)),
            set([Move.LEFT, Move.RIGHT]))
        self.assertEqual(snake_ai.best_move(), Move.LEFT.get_move())

    def test_go_for_further_tail(self):
        """Another snake is closer to the closest tail for snake."""
        curr_game = load_game('test_cases/go_for_further_tail.json')
        heuristic = Heuristic()
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertEqual(
            set(snake_ai.get_candidate_moves(curr_game.you, curr_game.board)),
            set([Move.LEFT, Move.RIGHT]))
        self.assertEqual(snake_ai.best_move(), Move.RIGHT.get_move())

    def test_follow_tail(self):
        """Follow tail of snake."""
        curr_game = load_game('test_cases/follow_tail.json')
        heuristic = Heuristic()
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertEqual(snake_ai.best_move(), Move.DOWN.get_move())

    def test_go_down_for_other_tail(self):
        """Follow tail of snake."""
        curr_game = load_game('test_cases/go_down_for_other_tail.json')
        heuristic = Heuristic()
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertEqual(
            set(snake_ai.get_candidate_moves(curr_game.you, curr_game.board)),
            set([Move.UP, Move.DOWN]))
        self.assertEqual(snake_ai.best_move(), Move.DOWN.get_move())

    def test_next_to_same_size_snake(self):
        """Going left will potentially crash into same size snake"""
        curr_game = load_game('test_cases/next_to_same_size_snake.json')
        heuristic = Heuristic()
        snake_ai = SnakeAI(curr_game, heuristic)
        self.assertNotEquals(snake_ai.best_move(), Move.LEFT.get_move())
