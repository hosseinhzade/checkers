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
