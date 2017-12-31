import unittest
import json
import os
from snakemodel.game import Game
from snakemodel.snake import Move

dir = os.path.dirname(__file__)


class TestBoardTransition(unittest.TestCase):
    """Tests for the simulating board transitions."""

    def test_basic(self):
        """Happy flow test."""
        basic_file = os.path.join(dir, 'test_cases/basic.json')
        basic_next_file = os.path.join(dir, 'test_cases/basic_next.json')
        with open(basic_file, "r") as (
            basic), open(basic_next_file, 'r') as (
                basic_next):
            basic_game = Game(json.load(basic))
            basic_next_game = Game(json.load(basic_next))
            my_snake_id = basic_game.you
            self.assertEqual(
                basic_game.simulate_moves(
                    basic_game.board,
                    {my_snake_id:
                     Move.RIGHT,
                     basic_next_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.DOWN}), basic_next_game.board)

    def test_collision(self):
        """Test collision between heads."""
        collision_file = os.path.join(dir, 'test_cases/collision.json')
        collision_next_file = os.path.join(
            dir,
            'test_cases/collision_next.json')
        with open(collision_file, "r") as (
            collision), open(collision_next_file, 'r') as (
                collision_next):
            collision_game = Game(json.load(collision))
            collision_next_game = Game(json.load(collision_next))
            my_snake_id = collision_game.you
            self.assertEqual(
                collision_game.simulate_moves(
                    collision_game.board,
                    {my_snake_id:
                     Move.DOWN,
                     collision_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.UP}), collision_next_game.board)
