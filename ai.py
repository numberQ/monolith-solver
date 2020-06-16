import draw_utils
from copy import deepcopy
import random
import timeit


MAX_DEPTH = 5


class AI:

    def __init__(self, boardwindow, msgwindow):
        self.boardwindow = boardwindow
        self.msgwindow = msgwindow
        self.path = []

    def pick_monomino(self, board):

        start_time = timeit.default_timer()

        best_score, best_monomino = self.find_best_path(board, 0)

        end_time = timeit.default_timer()

        draw_utils.update_message(self.msgwindow, "time taken to select move: " + str(end_time - start_time))

        return best_monomino

    def find_best_path(self, board, depth):

        best_score = board.get_score()
        best_monomino = None

        if board.is_board_done() or depth > MAX_DEPTH:
            return best_score, best_monomino

        already_checked = []

        for row in range(board.height):
            for col in range(board.width):

                monomino = board.get_monomino(row, col)

                if monomino in already_checked:
                    continue
                if monomino.is_empty():
                    continue
                original_selected_polymino = board.find_polymino(row, col)
                if len(original_selected_polymino) == 1:
                    continue

                [already_checked.append(monomino) for monomino in original_selected_polymino]

                test_board = deepcopy(board)
                test_board.selected_polymino = test_board.find_polymino(row, col)
                test_board.execute_selection()

                test_score, found_monomino = self.find_best_path(test_board, depth + 1)

                if test_score == best_score:
                    best_monomino = random.choice((best_monomino, monomino))
                elif test_score > best_score:
                    best_monomino = monomino
                    best_score = test_score

        draw_utils.update_board(self.boardwindow, board)
        self.boardwindow.refresh()

        return best_score, best_monomino
