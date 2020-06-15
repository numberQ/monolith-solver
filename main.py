import sys
import csv
from curses import wrapper
from game import Game


def main(stdscr):
    stdscr.clear()

    # If there is an argument, use that
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    # If not, let's just use a default
    else:
        filepath = "layout.csv"

    board = list(csv.reader(open(filepath)))

    game = Game(board, stdscr)
    game.init_game()


wrapper(main)
