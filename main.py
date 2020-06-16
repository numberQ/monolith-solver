import sys
import csv
from curses import wrapper
from game import Game
import random
from monomino import MinoType


def main(stdscr):
    stdscr.clear()

    # If there is an argument, use that
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        plain_board = list(csv.reader(open(filepath)))
    # If not, let's just use a default
    else:
        height = 11
        width = 22
        plain_board = random_board(height, width)

    game = Game(plain_board, stdscr)
    game.init_game()


def random_board(height, width):
    return [[random.randrange(1, MinoType.MAX_TYPE.value + 1) for col in range(width)] for row in range(height)]


wrapper(main)
