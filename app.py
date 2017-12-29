import os
import json
from snakeai.heuristic import Heuristic
from snakeai.snake_ai import SnakeAI
from snakemodel.game import Game
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/start", methods=["POST"])
def start():
    # NOTE: 'request' contains the data which was sent to us about the Snake
    # game after every POST to our server
    app.logger.info(request.__dict__)
    snake = {
        "color": os.environ.get('color', '#ffffff'),
        "name": os.environ.get('name', 'default_snake_boi'),
    }

    return jsonify(snake)


@app.route("/move", methods=["POST"])
def move():

    data = json.loads(request.data.decode("utf-8"))
    game = Game(data)
    heuristic = Heuristic()
    snake_ai = SnakeAI(game, heuristic)
    best_move = snake_ai.best_move()

    response = {
        "move": best_move
    }
    app.logger.debug(best_move)
    return jsonify(response)


if __name__ == "__main__":
    print("Starting server...")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
