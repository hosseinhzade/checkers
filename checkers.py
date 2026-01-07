import copy

# Constants
EMPTY = 0
BLACK = 1
WHITE = 2
BLACK_KING = 3
WHITE_KING = 4

BLACK_PLAYER = 'BLACK'
WHITE_PLAYER = 'WHITE'

# Directions
DIR_BLACK = [(1, -1), (1, 1)]     
DIR_WHITE = [(-1, -1), (-1, 1)]   
DIR_KING = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

BOARD_SIZE = 6

class Board:
    def __init__(self):
        self.board = [[-1]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 != 0:
                    self.board[r][c] = EMPTY
        # place black pieces
        for r in [0,1]:
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    self.board[r][c] = BLACK
        # place white pieces
        for r in [4,5]:
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    self.board[r][c] = WHITE

