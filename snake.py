# Based on the following repository
# https://github.com/techwithtim/Snake-Game/blob/master/snake.py

import pygame
import random
from copy import deepcopy
import searchproblem
from util import Action
from search import *
from setup import *
from util import Log


class Game:
    def __init__(self, window, snake):
        self.win = window
        self.snake = snake
        self.food = self.random_food()
        self.score = 0

    def get_state(self):
        # Call .pos for position (x, y)
        return {'snake': self.snake.snake_copy(),
                'food': self.food.pos}

    def get_new_state(self, state, action):
        successor_snake = state['snake'].snake_copy()
        successor_snake.discrete_move(action)
        return {'snake': successor_snake,
                'food': state['food']}

    def random_food(self):
        # Find random (x,y)
        # Error checking - inside border, not on top of snake body
        snake_positions = [sq.pos for sq in self.snake.body]
        while True:
            food_x = random.randint(1, ROWS-1)
            food_y = random.randint(1, COLS-1)
            if (food_x, food_y) not in snake_positions:
                break
        new_food = Square((food_x, food_y), GREEN, Action.STOP)
        self.food = new_food
        return new_food

    def redraw_window(self):
        self.win.fill(BLACK)
        self.snake.draw_snake(self.win)
        # Draw Food
        if not self.food:
            food = self.random_food()

        self.food.draw_square(self.win)
        self.draw_grid()
        pygame.display.update()

    def draw_grid(self):
        x = 0
        y = 0
        for i in range(ROWS):
            x += CELL_SIZE
            y += CELL_SIZE
            pygame.draw.line(self.win, WHITE, (x, 0), (x, WIDTH))
            pygame.draw.line(self.win, WHITE, (0, y), (WIDTH, y))

    def food_eaten(self, head_pos):
        if self.food:
            return head_pos == self.food.pos
        return False


class Snake:
    def __init__(self, head_pos, head_color, body_color):
        self.origin = head_pos
        self.direction = Action.STOP
        self.head_color = head_color
        self.body_color = body_color
        self.head = Square(head_pos, head_color, self.direction)
        self.body = [self.head]
        self.turns = {}

    def snake_copy(self):
        copy = Snake(self.head.pos, self.head_color, self.body_color)
        # copy.head = Square(self.head.pos, self.head_color, self.direction)
        copy.body = deepcopy(self.body)
        copy.head = copy.body[0]
        copy.turns = deepcopy(self.turns)
        return copy



    def reset(self):
        self.direction = Action.STOP
        self.head = Square(self.origin, self.head_color, self.direction)
        self.body = [self.head]
        self.turns = {}

    def keyboard_move(self):
        # Detect a key press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            valid_press = False
            # Can use directional arrows or WASD
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction = Action.LEFT
                valid_press = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction = Action.RIGHT
                valid_press = True
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction = Action.UP
                valid_press = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction = Action.DOWN
                valid_press = True
            # Update turns dictionary if a valid press occurred
            if valid_press:
                self.turns[self.head.pos[:]] = self.direction
        self.snake_move()

    # TODO work in progress
    def discrete_move(self, action):
        pygame.event.get()
        self.direction = action
        self.turns[self.head.pos[:]] = self.direction
        self.snake_move()

    def snake_move(self):
        # Redirect body segments to follow the turns made by the head
        for i, segment in enumerate(self.body):
            pos = segment.pos
            if pos in self.turns:
                # Set the action stored in turns dict for this position
                segment.change_direction(self.turns[pos])
                # After last segment passes, forget the turn
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            # Always move every segment
            segment.move()

    def add_segment(self):
        previous_tail = self.body[-1]
        direction = previous_tail.direction
        segment_pos = (previous_tail.pos[0] - direction.value[0],
                       previous_tail.pos[1] - direction.value[1])
        self.body.append(Square(segment_pos, self.body_color, direction))

    def draw_snake(self, window):
        for segment in self.body:
            segment.draw_square(window)

    def body_collide(self):
        body_positions = [sq.pos for sq in self.body]
        body_positions.remove(self.head.pos)
        return self.head.pos in body_positions

    def wall_collide(self):
        # Check if out of bounds on any side
        head_pos = self.body[0].pos
        return (head_pos[0] < 0) or (head_pos[0] > ROWS - 1) or (head_pos[1] < 0) or (head_pos[1] > COLS - 1)


class Square:
    def __init__(self, pos, color, action):
        self.pos = pos
        self.color = color
        self.direction = action

    def __str__(self):
        return str(self.pos)

    def change_direction(self, action):
        self.direction = action

    def move(self):
        self.pos = (self.pos[0] + self.direction.value[0], self.pos[1] + self.direction.value[1])

    def draw_square(self, window):
        pygame.draw.rect(window, self.color,
                         (self.pos[0] * CELL_SIZE + 1,
                          self.pos[1] * CELL_SIZE + 1,
                          CELL_SIZE - 2,
                          CELL_SIZE - 2))

    def get_pos(self):
        return self.pos



# The original driver
def manual_game():
    snake = Snake(START_POS, RED,RED)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(window, snake)
    game.redraw_window()
    clock = pygame.time.Clock()

    counter = 0
    while True:
        pygame.time.delay(50)
        clock.tick(10)

        game.snake.keyboard_move()

        if game.snake.wall_collide():
            print("DEATH -- WALL COLLIDE -- GAME OVER")
            break

        if game.snake.body_collide():
            print("DEATH -- BODY COLLIDE -- GAME OVER")
            break

        if game.food_eaten(snake.head.pos):
            # increment score
            game.score += 1
            print("Score:", game.score)
            # add body segment
            game.snake.add_segment()
            # generate new food
            game.random_food()

        game.redraw_window()
        counter += 1


# TODO food right next to body encounters infinite loop because no moves are selected
def search_driver(function, heuristic=util.manhattanDistance):
    snake = Snake(START_POS, WHITE, RED)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(window, snake)
    game.redraw_window()
    clock = pygame.time.Clock()
    dead = False

    log = Log(function.__name__, heuristic.__name__)

    while not dead:
        # initialize search problem

        log.start_stopwatch()
        problem = searchproblem.SimpleSearchProblem(game, game.get_state())
        moves = function(problem, heuristic)
        print(moves)

        log.stop_stopwatch()

        for i in range(len(moves)):

            pygame.time.delay(50)
            clock.tick(10)
            game.snake.discrete_move(moves[i])
            if game.snake.wall_collide():
                print("DEATH -- WALL COLLIDE -- GAME OVER")
                dead = True
                log.terminate("Wall Collision")
                break

            if game.snake.body_collide():
                print("DEATH -- BODY COLLIDE -- GAME OVER")
                dead = True
                log.terminate("Body Collision")
                break

            if game.food_eaten(snake.head.pos):
                # increment score
                game.score += 1
                print("Score:", game.score)

                log.update(game.score)

                # add body segment
                game.snake.add_segment()
                # generate new food
                game.random_food()

            game.redraw_window()

    print("FINAL SCORE:", game.score)
    print(log)
    return log



#log = search_driver(dls)
#log.save("log.txt")
#manual_game()


def no_display_run(function, run_number, heuristic=util.manhattanDistance):
    print("Begin Run " + str(run_number)+ " of "+ str(function.__name__))
    snake = Snake(START_POS, WHITE, RED)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(window, snake)
    dead = False
    log = Log(function.__name__, heuristic.__name__)
    while not dead:
        # initialize search problem
        log.start_stopwatch()
        problem = searchproblem.SimpleSearchProblem(game, game.get_state())
        moves = function(problem, heuristic)
        log.stop_stopwatch()

        for i in range(len(moves)):
            game.snake.discrete_move(moves[i])
            if game.snake.wall_collide():
                dead = True
                log.terminate("Wall Collision")
                break
            if game.snake.body_collide():
                dead = True
                log.terminate("Body Collision")
                break
            if game.food_eaten(snake.head.pos):
                # increment score
                game.score += 1
                log.update(game.score)
                # add body segment
                game.snake.add_segment()
                # generate new food
                game.random_food()
    print("End Run " + str(run_number) + " of " + str(function.__name__) + " with score " + str(game.score))
    return log


def gather_empirical_data():
    # Run the given number of tests on each algorithm, saving the results under the given filename
    for i in range(len(ALGORITHMS)):
        for j in range(NUM_TESTS):
            log = no_display_run(ALGORITHMS[i][0], j + 1, ALGORITHMS[i][1])
            log.save(ALGORITHMS[i][2])


def parse_empirical_data():
    # Header with information about the current automated test run
    data_file = open("data/results.txt", 'a')
    data_file.write("----- BEGINNING OF AUTOMATED TESTING SESSION -----\n")
    data_file.write("Rows:    " + str(ROWS) + "\n")
    data_file.write("Columns: " + str(COLS) + "\n")
    data_file.write("Number of Tests: " + str(NUM_TESTS) + "\n")
    data_file.write("\n---\n")
    # Extracting the names of the files to parse
    log_files = []
    for entry in ALGORITHMS:
        log_files.append(entry[2])
    # Analyze information for each file
    for filename in log_files:
        log = open(filename, 'r')
        line_list = log.readlines()
        log.close()
        # Accumulating the score and average turn time per game
        total_score = 0
        total_avg_time = 0
        # Keep track of the [high/low] x [score/turn time] for each algorithm file
        high_score = float('-inf')
        low_score = float('inf')
        longest_turn = float('-inf')
        shortest_turn = float('inf')
        for line in line_list:
            words = line.split(" ")
            if words[0] == "Score:":
                total_score += int(words[1])
                if int(words[1]) > high_score:
                    high_score = int(words[1])
                elif int(words[1]) < low_score:
                    low_score = int(words[1])
            elif words[0] == "Average":
                total_avg_time += float(words[2])
                if float(words[2]) > longest_turn:
                    longest_turn = float(words[2])
                elif float(words[2]) < shortest_turn:
                    shortest_turn = float(words[2])
        # Record the calculations in the results file
        data_file.write(line_list[0])
        data_file.write(line_list[1])
        data_file.write("Average Turn Time:  " + str(total_avg_time / NUM_TESTS) + "\n")
        data_file.write("Fastest Turn Time:  " + str(shortest_turn) + "\n")
        data_file.write("Longest Turn Time:  " + str(longest_turn) + "\n")
        data_file.write("Average Game Score: " + str(total_score / NUM_TESTS) + "\n")
        data_file.write("High Score:         " + str(high_score) + "\n")
        data_file.write("Low Score:          " + str(low_score) + "\n")
        data_file.write("---\n")

    data_file.write("----- END OF AUTOMATED TESTING SESSION -----\n\n\n")
    data_file.close()


# Used to run automated testing
# DFS, DLS, BFS, BFS+, UCS, UCS+, [A-star, A-star+, Greedy, Greedy+] x [Manhattan Distance, Food Trapped]
# Still some issue with DFS? (dfs, util.manhattanDistance, "data/dfs_log.txt"),
ALGORITHMS = [(dls, util.manhattanDistance, "data/dls_log.txt"),
              (bfs, util.manhattanDistance, "data/bfs_log.txt"),
              (bfs_plus, util.manhattanDistance, "data/bfs_plus_log.txt"),
              (ucs, util.manhattanDistance, "data/ucs_log.txt"),
              (ucs_plus, util.manhattanDistance, "data/ucs_plus_log.txt"),
              (astar, util.manhattanDistance, "data/astar_manhattan_log.txt"),
              (astar, util.foodTrappedHeuristic, "data/astar_food_trapped_log.txt"),
              (astar_plus, util.manhattanDistance, "data/astar_plus_manhattan_log.txt"),
              (astar_plus, util.foodTrappedHeuristic, "data/astar_plus_food_trapped_log.txt"),
              (greedy, util.manhattanDistance, "data/greedy_manhattan_log.txt"),
              (greedy, util.foodTrappedHeuristic, "data/greedy_food_trapped_log.txt"),
              (greedy_plus, util.manhattanDistance, "data/greedy_plus_manhattan_log.txt"),
              (greedy_plus, util.foodTrappedHeuristic, "data/greedy_plus_food_trapped_log.txt")]

NUM_TESTS = 500

#gather_empirical_data()
parse_empirical_data()
