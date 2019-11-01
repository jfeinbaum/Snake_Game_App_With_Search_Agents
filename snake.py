# Based on the following repository
# https://github.com/techwithtim/Snake-Game/blob/master/snake.py

import pygame
import random
import time
from enum import Enum

# Game Dimensions (rows & cols should evenly divide game board)
WIDTH = 600
HEIGHT = 600
ROWS = 30
COLS = 30
CELL_SIZE = WIDTH // ROWS
# Color tuples
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:
    def __init__(self, window, snake):
        self.win = window
        self.snake = snake
        self.food = None
        self.score = 0


    def random_food(self):
        # Find random (x,y)
        # Error checking - inside border, not on top of snake body
        snake_positions = [sq.pos for sq in self.snake.body]
        while True:
            food_x = random.randint(0, ROWS)
            food_y = random.randint(0, COLS)
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

    def wall_collide(self, head_pos):
        # Check if out of bounds on any side
        return (head_pos[0] < 0) or (head_pos[0] > ROWS) or (head_pos[1] < 0) or (head_pos[1] > COLS)

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

        # Redirect body segments to follow the turns made by the head
        for i, segment in enumerate(self.body):
            pos = segment.pos
            if pos in self.turns:
                # Set the action stored in turns dict for this position
                segment.change_direction(self.turns[pos])
                # After last segment passes, forget the turn
                # TODO Turns to follow path of head square are not properly forgotten
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            # Always move every segment
            segment.move()

    def add_segment(self):
        # TODO segments should not be able to disconnect from the head of the snake
        previous_tail = self.body[-1]
        direction = previous_tail.direction
        segment_pos = (previous_tail.pos[0] - direction.value[0],
                       previous_tail.pos[1] - direction.value[1])
        self.body.append(Square(segment_pos, self.body_color, direction))



    def draw_snake(self, window):
        for segment in self.body:
            segment.draw_square(window)

    def body_collide(self):
        # TODO implement body collision
        return False


class Square:
    def __init__(self, pos, color, action):
        self.pos = pos
        self.color = color
        self.direction = action

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


class Action(Enum):
    # Also referred to as direction,
    # Up and down are inverted here to reflect the graphics on the screen
    # Use .value[0] and .value[1] to access x,y from an action enum
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STOP = (0, 0)


def driver():
    snake = Snake((10, 10), RED, WHITE)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(window, snake)
    game.redraw_window()
    clock = pygame.time.Clock()





    while True:
        pygame.time.delay(50)
        clock.tick(10)
        game.snake.keyboard_move()
        if game.wall_collide(snake.head.pos):
            print("DEATH -- WALL COLLIDE -- GAME OVER")
            break

        if game.snake.body_collide():
            print("DEATH -- BODY COLLIDE -- GAME OVER")
            break

        # TODO eat food -> add body segment, increment score counter
        if game.food_eaten(snake.head.pos):
            # increment score
            game.score += 1
            print("Score:", game.score)
            # add body segment
            game.snake.add_segment()


            # generate new food
            game.random_food()






        game.redraw_window()




driver()