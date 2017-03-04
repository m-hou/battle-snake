from flask import Flask, request, jsonify
import random
import datetime
import logging

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

    #print(request.__dict__)
    moves = ["up", "down", "left", "right"]
    move = random.choice(moves)
    response = {
        "move": move
    }
    app.logger.debug(move)
    return jsonify(response)

if __name__ == "__main__":
    print("Starting server...")
    app.run(port=8080, debug=True)
