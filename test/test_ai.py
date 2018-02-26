import unittest
import json
import os
from snakemodel.game import Game
from snakemodel.snake import Move
from snakeai.snake_ai import SnakeAI
from snakeai.heuristic import Heuristic

dir = os.path.dirname(__file__)


class TestSnakeAI(unittest.TestCase):
    """Tests for SnakeAI logic."""

    def test_one_candidate_move(self):
        """Test get_candidate_moves where there is only 1 available move."""
        one_available_move_file = os.path.join(
            dir,
            'test_cases/one_available_move.json')
        with open(one_available_move_file, "r") as one_available_move:
            game = Game(json.load(one_available_move))
            heuristic = Heuristic()
            snake_ai = SnakeAI(game, heuristic)
            self.assertEqual(
                snake_ai.get_candidate_moves(game.you, game.board),
                [Move.DOWN])

    def test_candidate_move_heads_diagonal(self):
        """Test get_candidate_moves where 2 snakes are diagonally adjacent."""
        diagonal_head_file = os.path.join(
            dir,
            'test_cases/diagonal_head.json')
        with open(diagonal_head_file, "r") as diagonal_head:
            game = Game(json.load(diagonal_head))
            heuristic = Heuristic()
            snake_ai = SnakeAI(game, heuristic)
            self.assertEqual(
                snake_ai.get_candidate_moves(game.you, game.board),
                [Move.DOWN])

    def test_corner(self):
        """
        Test case where going up will eat food but put snake in a corner
        (i.e. next turn death).

        Only move is to move down.
        """
        corner_file = os.path.join(
            dir,
            'test_cases/corner.json')
        with open(corner_file, "r") as corner:
            game = Game(json.load(corner))
            heuristic = Heuristic()
            snake_ai = SnakeAI(game, heuristic)
            self.assertEqual(snake_ai.best_move(), Move.DOWN.get_move())

    def test_go_for_food(self):
        """Test case where snake should go for food."""
        corner_file = os.path.join(
            dir,
            'test_cases/go_for_food.json')
        with open(corner_file, "r") as corner:
            game = Game(json.load(corner))
            heuristic = Heuristic()
            snake_ai = SnakeAI(game, heuristic)
            self.assertEqual(snake_ai.best_move(), Move.DOWN.get_move())
