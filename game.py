from board import Board
from copy import deepcopy
import curses
import draw_utils
from monomino import MinoType


class Game:

    def __init__(self, plain_board, stdscr):
        self.board = Board(plain_board)
        self.stdscr = stdscr
        self.boardwindow = None
        self.msgwindow = None
        self.errwindow = None
        self.history = [deepcopy(self.board)]
        self.history_idx = 0

    def init_game(self):

        curses.init_color(draw_utils.COLOR_GREY, 500, 500, 500)
        curses.init_pair(MinoType.GREY.value, curses.COLOR_BLACK, draw_utils.COLOR_GREY)
        curses.init_pair(MinoType.RED.value, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(MinoType.YELLOW.value, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(MinoType.BLUE.value, curses.COLOR_BLACK, curses.COLOR_BLUE)

        self.boardwindow = curses.newwin(self.board.height + 2, self.board.width + 2, 0, 0)
        self.msgwindow = curses.newwin(10, 100, self.board.height + 2, 0)
        self.errwindow = curses.newwin(10, 111, self.board.height + 12, 0)

        self.board.move(0, 0)
        draw_utils.update_message("Use arrow keys to select polynimo. Press ENTER to select.\n"
                                  "'u' to undo and 'r' to redo.", self.msgwindow)

        self.game_loop()

    def game_loop(self):

        game_over = False
        while not game_over:

            draw_utils.update_board(self.board, self.boardwindow)

            self.stdscr.refresh()
            self.boardwindow.refresh()
            self.msgwindow.refresh()
            self.errwindow.refresh()

            key = self.stdscr.getch()

            self.errwindow.clear()

            if key == curses.KEY_UP:
                self.board.move(0, -1)
            if key == curses.KEY_DOWN:
                self.board.move(0, 1)
            if key == curses.KEY_LEFT:
                self.board.move(-1, 0)
            if key == curses.KEY_RIGHT:
                self.board.move(1, 0)

            if key == ord('u'):
                self.undo_history()
            if key == ord('r'):
                self.redo_history()

            if key == curses.KEY_ENTER or key == 10 or key == 13:
                if len(self.board.selected_polymino) == 0:
                    draw_utils.update_message("Cannot select an empty cell!", self.errwindow)
                elif len(self.board.selected_polymino) == 1:
                    draw_utils.update_message("Cannot select a 1-cell polymino!", self.errwindow)
                else:
                    self.board.execute_selection()
                    self.add_history()

    def undo_history(self):
        if self.history_idx == 0:
            draw_utils.update_message("Cannot undo before initial board state!", self.errwindow)
            return
        self.history_idx -= 1
        self.set_history()

    def redo_history(self):
        if self.history_idx == len(self.history) - 1:
            draw_utils.update_message("Cannot redo past most recent board state!", self.errwindow)
            return
        self.history_idx += 1
        self.set_history()

    def set_history(self):
        user_row = self.board.user_row
        user_col = self.board.user_col
        self.board = deepcopy(self.history[self.history_idx])
        self.board.user_row = user_row
        self.board.user_col = user_col

    def add_history(self):
        if self.history_idx < len(self.history) - 1:
            slice_end = self.history_idx + 1
            self.history = self.history[:slice_end]
        self.history.append(deepcopy(self.board))
        self.history_idx += 1
