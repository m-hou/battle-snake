import unittest
from snakemodel.snake import Move
from snakeai.snake_ai import SnakeAI
from snakeai.heuristic import Heuristic
from .test_util import load_game


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


    def test_trap(self):
        game = load_game('test_cases/psuedo_trap.json')
        h = Heuristic(2)
        snake = SnakeAI(game, h)
        moves = snake.best_move()
        # candidate = snake.get_candidate_moves(game.you, game.board)
        self.assertEqual(moves, 'right')


    def test_collision(self):
        game = load_game('test_cases/collision.json')
        h = Heuristic(1)
        snake = SnakeAI(game, h)
        moves = snake.best_move()
        # candidate = snake.get_candidate_moves(game.you, game.board)

        self.assertEqual(moves, 'left')

    def test_selfcollision(self):
        game = load_game('test_cases/sadsnake.json')
        h = Heuristic(1)
        snake = SnakeAI(game, h)
        moves = snake.best_move()
        candidate = snake.get_candidate_moves(game.you, game.board)
        print("candidates are here",  candidate)
        print(moves)
