from board import Board
from copy import deepcopy
import curses
import draw_utils
from monomino import MinoType
from ai import AI


class Game:

    def __init__(self, plain_board, stdscr):
        self.board = Board(plain_board)
        self.stdscr = stdscr
        self.boardwindow = None
        self.msgwindow = None
        self.errwindow = None
        self.history = [deepcopy(self.board)]
        self.history_idx = 0
        self.ai = None

    def init_game(self):

        curses.init_color(draw_utils.COLOR_GREY, 500, 500, 500)
        curses.init_pair(MinoType.GREY.value, curses.COLOR_BLACK, draw_utils.COLOR_GREY)
        curses.init_pair(MinoType.RED.value, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(MinoType.YELLOW.value, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(MinoType.BLUE.value, curses.COLOR_BLACK, curses.COLOR_BLUE)

        self.boardwindow = curses.newwin(self.board.height + 2, self.board.width + 2, 0, 0)
        self.msgwindow = curses.newwin(10, 100, self.board.height + 2, 0)
        self.errwindow = curses.newwin(10, 111, self.board.height + 12, 0)

        self.ai = AI(self.boardwindow, self.msgwindow)

        self.board.move(0, 0)

        draw_utils.update_message(self.msgwindow,
                                  "Use arrow keys to select polymino. Press ENTER to select.",
                                  "Or press SPACE to let the AI take over.",
                                  "'u' to undo and 'r' to redo.",
                                  "Press 'q' at any time to quit.")

        self.game_loop()

    def game_loop(self):

        key = None
        game_over = False

        while not game_over or key != ord('q'):

            draw_utils.update_board(self.boardwindow, self.board)

            self.stdscr.refresh()
            self.boardwindow.refresh()
            self.msgwindow.refresh()
            self.errwindow.refresh()

            key = self.stdscr.getch()

            self.errwindow.clear()

            if key == ord('q'):
                game_over = True

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
                    draw_utils.update_message(self.errwindow, "Cannot select an empty cell!")
                elif len(self.board.selected_polymino) == 1:
                    draw_utils.update_message(self.errwindow, "Cannot select a 1-cell polymino!")
                else:
                    self.board.execute_selection()
                    self.add_history()

            # Let the AI take over
            if key == ord(' '):
                monomino = self.ai.pick_monomino(self.board)
                draw_utils.update_message(self.errwindow, "(" + str(monomino.row) + "," + str(monomino.col) + ")")
                if monomino is None:
                    draw_utils.update_message(self.errwindow, "Could not find a move.")
                else:
                    self.board.get_monomino(self.board.user_row, self.board.user_col).unselect()
                    self.board.user_row = monomino.row
                    self.board.user_col = monomino.col
                    self.board.move(0, 0)
                # if len(self.board.selected_polymino) == 0:
                #     draw_utils.update_message(self.errwindow, "Cannot select an empty cell!")
                # elif len(self.board.selected_polymino) == 1:
                #     draw_utils.update_message(self.errwindow, "Cannot select a 1-cell polymino!")
                # else:
                #     self.board.execute_selection()
                #     self.add_history()

            if self.board.is_board_done():
                draw_utils.update_message(self.errwindow, "No valid moves remain. You must either undo or quit.")

    def undo_history(self):
        if self.history_idx == 0:
            draw_utils.update_message(self.errwindow, "Cannot undo before initial board state!")
            return
        self.history_idx -= 1
        self.set_history()

    def redo_history(self):
        if self.history_idx == len(self.history) - 1:
            draw_utils.update_message(self.errwindow, "Cannot redo past most recent board state!")
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
