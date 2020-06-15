import curses

COLOR_GREY = 100


def update_board(board, scr):
    for row in range(board.height):
        for col in range(board.width):
            monomino = board.get_monomino(row, col)
            mino_type = monomino.mino_type.value
            color_pair = curses.color_pair(mino_type)
            if monomino.row == board.user_row and monomino.col == board.user_col:
                color_pair |= curses.A_BLINK | curses.A_STANDOUT
            elif monomino.selected:
                color_pair |= curses.A_BLINK
            scr.addstr(row + 1, col + 1, str(mino_type), color_pair)


def update_message(message, scr):
    scr.clear()
    scr.addstr(1, 1, str(message))
