import json
import os
from snakemodel.game import Game

dir = os.path.dirname(__file__)


def load_game(file_name):
    """Happy flow test."""
    game_file = os.path.join(dir, file_name)
    with open(game_file, "r") as game_data:
        return Game(json.load(game_data))
