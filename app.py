import os
import json
import logging
from snakeai.heuristic import Heuristic
from snakeai.snake_ai import SnakeAI
from snakemodel.game import Game
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/start", methods=["POST"])
def start():
    # NOTE: 'request' contains the data which was sent to us about the Snake
    # game after every POST to our server
    snake = {
        "color": "#ffffff",
        "name": "My Snake's Name!"
    }

    return jsonify(snake)


@app.route("/move", methods=["POST"])
def move():
    data = json.loads(request.data.decode("utf-8"))
    game = Game(data)
    heuristic = Heuristic()
    snake_ai = SnakeAI(game, heuristic)
    best_move = snake_ai.best_move()

    app.logger.debug("{} \n {}".format(data, best_move))
    response = {
        "move": best_move
    }
    return jsonify(response)


if __name__ == "__main__":
    print("Starting server...")
    port = int(os.environ.get("PORT", 8080))
    debug = bool(os.environ.get("DEBUG", True))
    handler = RotatingFileHandler("debug.log")
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=port, debug=debug)
