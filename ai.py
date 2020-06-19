import draw_utils
from copy import deepcopy
import random
import timeit
from state_tree import Node


MAX_DEPTH = 3
MAX_DISTANCE = 3


class AI:

    def __init__(self, boardwindow, msgwindow):
        self.boardwindow = boardwindow
        self.msgwindow = msgwindow

    def pick_monomino(self, board):

        start_time = timeit.default_timer()

        best_score, best_monomino, root_node = self.find_best_path(board, 0, [], None)

        end_time = timeit.default_timer()

        draw_utils.update_message(self.msgwindow, "time taken to select path: " + str(end_time - start_time))

        return root_node

    def find_best_path(self, board, depth, previous_polymino, node):

        best_score = board.get_score()
        best_monomino = None
        best_node = None

        if board.is_board_done() or depth > MAX_DEPTH:
            return best_score, best_monomino, node

        already_checked = []

        for row in range(board.height):
            for col in range(board.width):

                monomino = board.get_monomino(row, col)

                if monomino in already_checked:
                    continue
                if monomino.is_empty():
                    continue

                too_far = True
                for m in previous_polymino:
                    if abs(m.row - row) < MAX_DISTANCE and abs(m.col - col) < MAX_DISTANCE:
                        too_far = False
                        break

                if too_far and len(previous_polymino) > 0:
                    continue

                previous_polymino = deepcopy(board.find_polymino(row, col))
                if len(previous_polymino) == 1:
                    continue

                [already_checked.append(monomino) for monomino in previous_polymino]

                test_board = deepcopy(board)
                test_board.selected_polymino = test_board.find_polymino(row, col)
                test_board.execute_selection()

                test_score, _, test_node = self.find_best_path(test_board, depth + 1, previous_polymino, node)

                if test_score == best_score:
                    best_monomino = random.choice((best_monomino, monomino))
                    best_node = random.choice((best_node, test_node))
                elif test_score > best_score:
                    best_monomino = monomino
                    best_score = test_score
                    best_node = test_node

        if best_monomino is not None:
            best_coords = (best_monomino.row, best_monomino.col)
            new_node = Node(best_score, best_coords)
            new_node.insert(best_node)
            if node is None:
                node = new_node
            else:
                node.insert(new_node)

        return best_score, best_monomino, node
