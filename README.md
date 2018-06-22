# BattleSnake

BattleSnake was a project made for the [BattleSnake](https://www.battlesnake.io/) competition, a competetive multiplayer AI challenge where teams compete to play in a battle-royale variation of the classic game "snake". Many players participate and bring snakes with a variety of strategies and the tournament is played live at the [Victoria Convention Center](https://www.tourismvictoria.com/meetings/victoria-conference-centre). 

#### Challenges
__Highly configurable games__ - snakes have to be adaptive to a variety of game settings, such as board size and number of snakes and food on the board.
__Large search space__ - the tournament ran with 10 snakes on the board at the same time each with 4 possible moves to make. This lead to combinatorial explosion in the search space.
__Low latentcy__ - snakes must respond within 200ms per move

#### Architecture

The AI is deployed to Heroku as a REST API that communicated with the central game server. The project is made of two main modules:

__SnakeBoard__ - all the logic for generating board states and transitioning
__SnakeAI__ - all the logic for evaluating the board and picking the best move

The goal was to seperate the concerns of the model and the AI and to allow the AI to be flexible to modifications. Search depth and heuristic functions are all configurable.

#### Strategies
We went with a recursive heuristic search strategy at first. However, since we had a small Heroku instance, we quickly realized that even a frugal depth would timeout. Instead, we went for a one-depth search but with a involved heuristic that would "simulate" a look-ahead.

The heuristic is a hierarchal compostion of several tasks that the snake tries prioritize. For example, if going left versus going right lead to scores of 10 and 5 respectively on the first (highest priority) task, left would be the move. If however, the scores were both 10, the score for task 2 would be used to break the tie, and so on.

The tasks that were used in the final model (for the competition) were vonoroi partitioning, distance to tail, distance to food.

__Voronoi partitioning__ - this strategy revolves on the concept of a [voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram). The gist of it is to maximize the amount of squares that one is closer to. A snake with high-depth search and voronoi partitioning could essentially "box-out" the other player from territory and food.

__Distance to tail__ - looking at last year's competition, tail-chasing strategies dominated the scene. A snake would almost never get trapped if it chased its own tail, since they can move to the square that was previously occupied. Our snake was unique in that it would follow *any* tail within a threshold. The threshold is proportional to the health lost (how desperate the snake is for food), and being past the threshold would lead to a penalty from the heuristic. 

__Distance to food__ - snakes will starve if they spend 100 turns without eatting food. Also, snakes that have eaten more food will beat those that have eaten less in a head-to-head collision. We used the [A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) to calculate the distance.

__Reachable squares heuristic__ - we phased out a "reachable squares" heuristic as it was too expensive to compute. The strategy was to flood fill from the head to see how many squares are "reachable" (not obstructed by an obstacle). This heuristic is quite natural as it avoids dead ends; however, it does not paint the big picture. A snake that is tightly surrounded by obstacles is in a bad spot and is likely trapped, even if there is currently an opening.

__Claustophobic heuristic__ - this heuristic was not implemented due to time constraints; however, we speculate that it would be very effective. Essentially, we want to keep the head in an open space to promote having more options and safer gameplay. Playing defensively is important for the early game, when many snakes are on the board and the game is more volitile.

#### Shortcomings

__Performance__ - our snake's biggest weakness is lack of performance. Many top snakes were writen in faster programming languages, such as C++ and Go. Also, many were run on larger containers, giving them much more recursive depth in the search.

__Better heuristic__ - the meta-game changed a lot from last year. Once we got to the venue, we realized that tail chasing was out and voronoi partitioning was in. Our snake was tuned to do well against tail chasing but not prepared for new snakes running voronoi partitioning who were very effective at playing 1 vs. 1.

#### Special Thanks

__[ahendy](https://github.com/ahendy)__ - my teammate for the competition. He helped me brainstorm ideas and reviewed my code.

__[a1k0n](https://www.a1k0n.net/2010/03/04/google-ai-postmortem.html)__ - published a blog post with details about voronoi partitioning applied to another AI competition
