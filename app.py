import json
from snake_ai import SnakeAIv1
from game import Game
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/start", methods=["POST"])
def start():
    # NOTE: 'request' contains the data which was sent to us about the Snake
    # game after every POST to our server
    app.logger.info(request.__dict__)
    snake = {
        "color": "#ffffff",
        "name": "My Snake's Name!"
    }

    return jsonify(snake)


@app.route("/move", methods=["POST"])
def move():

    data = json.loads(request.data.decode("utf-8"))
    game = Game(data)
    snake_ai = SnakeAIv1(game)
    best_move = snake_ai.best_move()

    response = {
        "move": best_move
    }
    app.logger.debug(best_move)
    return jsonify(response)


if __name__ == "__main__":
    print("Starting server...")
    app.run(port=8080, debug=True)
