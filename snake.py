import pygame
import random
import time

WIDTH = 600
HEIGHT = 600
ROWS = 30
COLS = 30



class Game:
    def __init__(self, window):
        self.win = window

    def draw_grid(self):
        pass

class Snake:
    def __init__(self):
        pass

class Square:
    def __init__(self):
        pass



def driver():
    game = Game(pygame.display.set_mode((WIDTH, HEIGHT)))
    snake = Snake()

    time.sleep(2)

driver()