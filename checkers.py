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
    def print_board(self):
        print("  " + " ".join(str(c) for c in range(BOARD_SIZE)))
        for r in range(BOARD_SIZE):
            print(r, end=" ")
            for c in range(BOARD_SIZE):
                p = self.board[r][c]
                if p == -1:
                    print(".", end=" ")
                elif p == EMPTY:
                    print("_", end=" ")
                elif p == BLACK:
                    print("b", end=" ")
                elif p == WHITE:
                    print("w", end=" ")
                elif p == BLACK_KING:
                    print("B", end=" ")
                elif p == WHITE_KING:
                    print("W", end=" ")
            print()
        print()

    def copy(self):
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)
        return new_board

    def apply_move(self, move):
        piece = self.board[move[0][0]][move[0][1]]
        self.board[move[0][0]][move[0][1]] = EMPTY
        for i in range(1, len(move)):
            r_from, c_from = move[i-1]
            r_to, c_to = move[i]
            # capture
            if abs(r_to - r_from) == 2:
                r_mid = (r_to + r_from)//2
                c_mid = (c_to + c_from)//2
                self.board[r_mid][c_mid] = EMPTY
        r_end, c_end = move[-1]
        # promote to king
        if piece == BLACK and r_end == BOARD_SIZE-1:
            piece = BLACK_KING
        elif piece == WHITE and r_end == 0:
            piece = WHITE_KING
        self.board[r_end][c_end] = piece
        
    def get_legal_moves(self, player):
        moves = []
        max_captures = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece == EMPTY or piece == -1:
                    continue
                if player == BLACK_PLAYER and piece in [BLACK, BLACK_KING]:
                    piece_moves = self._get_piece_moves(r, c, piece)
                elif player == WHITE_PLAYER and piece in [WHITE, WHITE_KING]:
                    piece_moves = self._get_piece_moves(r, c, piece)
                else:
                    continue
                # اجباری بودن خوردن: بیشترین captures
                for m in piece_moves:
                    captures = max(len(m)-1,0)
                    if captures > max_captures:
                        max_captures = captures
                        moves = [m]
                    elif captures == max_captures:
                        moves.append(m)
        return moves




