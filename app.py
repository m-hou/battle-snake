from game import Game
from board import Board

from flask import Flask, request, jsonify
import random
import datetime
import logging
import json

app = Flask(__name__)

@app.route("/start", methods=["POST"])
def start():
    # NOTE: 'request' contains the data which was sent to us about the Snake game
    # after every POST to our server 
    app.logger.info(request.__dict__) 
    
    snake = {
        "color": "#ffffff",
        "name": "My Snake's Name!"
    }

    return jsonify(snake)

@app.route("/move", methods=["POST"])
def move():

    data = json.loads(request.data.decode("utf-8"))
    board = Board(data)
    game = Game(board)
    best_move = game.best_move()
    # my_snake = next(cell for cell in data["snakes"] if cell["id"] == data["you"])
    # my_head = my_snake["coords"][0]

    # target = data["food"][0]

    # move = "left"
    # if target[0] - my_head[0] < 0:
    #     move = "left"
    # elif target[0] - my_head[0] > 0:
    #     move = "right"
    # elif target[1] - my_head[1] < 0:
    #     move = "up"
    # elif target[1] - my_head[1] > 0:
    #     move = "down"

    response = {
        "move": best_move
    }
    app.logger.debug(move)
    return jsonify(response)

if __name__ == "__main__":
    print("Starting server...")
    app.run(port=8080, debug=True)
