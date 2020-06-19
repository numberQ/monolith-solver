import argparse
import csv
from curses import wrapper
from game import Game
import random
from monomino import MinoType
from board import Board


plain_board = []


def main(stdscr):
    stdscr.clear()

    game = Game(plain_board, stdscr)
    game.init_game()


def random_board(rows, cols):
    return [[random.randrange(1, MinoType.MAX_TYPE.value + 1) for col in range(cols)] for row in range(rows)]


parser = argparse.ArgumentParser(description="Helps solve the Monolith Treasure Hunter minigame from Danganronpa V3.")
parser.add_argument("-i", "--interactive",
                    help="Enables the interface which allows for user control, including undo and redo. "
                         "Leave disabled if you just want the AI to do its thing.",
                    action="store_true")
parser.add_argument("-f", "--file",
                    help="CSV file to load the board from. Otherwise, will generate a random board.")


args = parser.parse_args()

if args.file is not None:
    plain_board = list(csv.reader(open(args.file)))
else:
    height = 11
    width = 22
    plain_board = random_board(height, width)

if args.interactive:
    wrapper(main)
else:
    board = Board(plain_board)
    print("Board created:")
    [print(','.join([str(monomino.mino_type.value) for monomino in row])) for row in board.board]
