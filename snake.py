# Based on the following repository
# https://github.com/techwithtim/Snake-Game/blob/master/snake.py

import pygame
import random
from copy import deepcopy
import searchproblem
from util import Action
from search import *
from setup import *


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
        new_food = Square((food_x, food_y), WHITE, Action.STOP)
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
        return (head_pos[0] < 0) or (head_pos[0] > ROWS) or (head_pos[1] < 0) or (head_pos[1] > COLS)


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
def main():
    snake = Snake(START_POS, RED,RED)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(window, snake)
    game.redraw_window()
    clock = pygame.time.Clock()

    # initialize search problem
    problem = searchproblem.SimpleSearchProblem(game, game.get_state())
    moves = bfs(problem)
    print(moves)

    counter = 0
    while True:
        pygame.time.delay(50)
        clock.tick(10)

        #game.snake.keyboard_move()
        game.snake.discrete_move(moves[counter])
        print(counter)
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
def bfs_driver():
    snake = Snake(START_POS, RED,RED)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(window, snake)
    game.redraw_window()
    clock = pygame.time.Clock()
    dead = False

    while not dead:
        # initialize search problem
        problem = searchproblem.SimpleSearchProblem(game, game.get_state())
        moves = bfs(problem)
        #print(moves)

        for i in range(len(moves)):

            pygame.time.delay(50)
            clock.tick(10)

            #game.snake.keyboard_move()
            game.snake.discrete_move(moves[i])
            #print(i)
            if game.snake.wall_collide():
                print("DEATH -- WALL COLLIDE -- GAME OVER")
                dead = True
                break

            if game.snake.body_collide():
                print("DEATH -- BODY COLLIDE -- GAME OVER")
                dead = True
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


bfs_driver()
