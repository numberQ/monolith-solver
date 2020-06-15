from monomino import Monomino, MinoType


class Board:

    def __init__(self, board):
        self.height = len(board)
        self.width = len(board[0])
        self.board = self.init_board(board)

        self.user_col = 0
        self.user_row = 0

        self.selected_polymino = []

    def move(self, delta_col, delta_row):
        new_col = self.user_col + delta_col
        new_row = self.user_row + delta_row

        if new_col < 0 or new_col >= self.width:
            return
        if new_row < 0 or new_row >= self.height:
            return

        self.get_monomino(self.user_row, self.user_col).unselect()
        self.get_monomino(new_row, new_col).select()
        self.user_col = new_col
        self.user_row = new_row

        [monomino.unselect() for monomino in self.selected_polymino]

        self.find_polymino(new_row, new_col)

        [monomino.select() for monomino in self.selected_polymino]

    def get_monomino(self, row, col):
        return self.board[row][col]

    def init_board(self, board):
        new_board = []

        for row in range(self.height):
            new_row = []

            for col in range(self.width):
                monomino = Monomino(row, col, board[row][col])
                new_row.append(monomino)

            new_board.append(new_row)

        return new_board

    def find_polymino(self, row, col):
        selected_monomino = self.get_monomino(row, col)
        selected_mino_type = selected_monomino.mino_type

        if selected_mino_type == MinoType.EMPTY:
            self.selected_polymino = []
            return

        polymino = [selected_monomino]
        self.polymino_flood_fill(row, col, polymino, selected_mino_type)

        self.selected_polymino = polymino

    def polymino_flood_fill(self, row, col, polymino, mino_type):
        self.polymino_flood_fill_task(row - 1, col, polymino, mino_type)
        self.polymino_flood_fill_task(row + 1, col, polymino, mino_type)
        self.polymino_flood_fill_task(row, col - 1, polymino, mino_type)
        self.polymino_flood_fill_task(row, col + 1, polymino, mino_type)

    def polymino_flood_fill_task(self, row, col, polymino, mino_type):

        # Ensures we're not trying to check something outside the board
        if not self.on_board(row, col):
            return

        monomino_to_check = self.get_monomino(row, col)

        # Compares the mino type of the original selection to the monomino we're checking now
        if monomino_to_check.mino_type != mino_type:
            return

        # Checks if the monomino we're checking now has already been added to the mino
        if monomino_to_check in polymino:
            return

        # If we made it past all those conditions, we can safely add this to the polymino
        polymino.append(monomino_to_check)

        self.polymino_flood_fill(row, col, polymino, mino_type)

    def execute_selection(self):

        incremented = []

        for monomino in self.selected_polymino:

            monomino.empty()

            row = monomino.row
            col = monomino.col

            self.increment(row - 1, col, self.selected_polymino, incremented)
            self.increment(row + 1, col, self.selected_polymino, incremented)
            self.increment(row, col - 1, self.selected_polymino, incremented)
            self.increment(row, col + 1, self.selected_polymino, incremented)

        self.selected_polymino = []

    def increment(self, row, col, polymino, incremented):

        if not self.on_board(row, col):
            return

        monomino = self.get_monomino(row, col)

        if monomino in polymino or monomino in incremented:
            return

        monomino.increment()
        incremented.append(monomino)

    def on_board(self, row, col):

        if row < 0 or row >= self.height:
            return False
        if col < 0 or col >= self.width:
            return False

        return True

    def is_board_done(self):
        for row in range(self.height):
            for col in range(self.width):
                polymino = self.find_polymino(row, col)
                if len(polymino) > 1:
                    return False

        return True
