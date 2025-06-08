import pygame
import random
from copy import deepcopy

# Конфигурация
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

FPS = 60

COLORS = {
    "I": (0, 255, 255),
    "J": (0, 0, 255),
    "L": (255, 165, 0),
    "O": (255, 255, 0),
    "S": (0, 255, 0),
    "T": (128, 0, 128),
    "Z": (255, 0, 0),
    "BACKGROUND": (10, 10, 10),
    "GRID": (30, 30, 30),
}

SHAPES = {
    'I': [[1]][[1]][[1]][[1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}


class Tetromino:
    def init(self, shape=None):
        self.shape = shape or random.choice(list(SHAPES.keys()))
        self.matrix = SHAPES[self.shape]
        self.color = COLORS[self.shape]
        self.x = 3
        self.y = 0

    def rotate(self):
        self.matrix = [list(row) for row in zip(*self.matrix[::-1])]


class Grid:
    def init(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def is_valid_position(self, tetromino, offset_x=0, offset_y=0):
        for y, row in enumerate(tetromino.matrix):
            for x, cell in enumerate(row):
                if cell:
                    new_x = tetromino.x + x + offset_x
                    new_y = tetromino.y + y + offset_y
                    if new_x < 0 or new_x >= self.cols or new_y >= self.rows:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def place_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.matrix):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = tetromino.y + y
                    grid_x = tetromino.x + x
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = 1

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = len(self.grid) - len(new_grid)
        self.grid = [[0]*self.cols for _ in range(lines_cleared)] + new_grid
        return lines_cleared
