import random


class AI:
    def pick_monomino(self, board):

        if board.is_board_done():
            return

        keep_going = True
        while keep_going:
            rand_row = random.randrange(board.height)
            rand_col = random.randrange(board.width)
            board.selected_polymino = board.find_polymino(rand_row, rand_col)
            if len(board.selected_polymino) == 0:
                continue
            elif len(board.selected_polymino) == 1:
                continue

            break
