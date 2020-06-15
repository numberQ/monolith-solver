from enum import IntEnum


class MinoType(IntEnum):
    EMPTY = 0
    GREY = 1
    RED = 2
    YELLOW = 3
    BLUE = 4
    MAX_TYPE = 4


class Monomino:

    def __init__(self, row, col, num):
        (self.row, self.col) = row, col
        self.mino_type = MinoType(int(num))
        self.selected = False

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def empty(self):
        self.unselect()
        self.mino_type = MinoType.EMPTY

    def increment(self):

        current_type = self.mino_type

        if current_type == MinoType.EMPTY:
            return

        new_type = current_type + 1

        if current_type == MinoType.MAX_TYPE:
            new_type = 1

        self.mino_type = MinoType(new_type)
