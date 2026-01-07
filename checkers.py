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
    def _get_piece_moves(self, r, c, piece):
        # generate all capture moves first
        captures = []
        self._dfs_capture(r, c, piece, [(r,c)], captures, set())
        if captures:
            return captures  # اگر capture موجود است، اجباری است
        # اگر capture نیست، حرکات ساده
        moves = []
        directions = DIR_KING if piece in [BLACK_KING, WHITE_KING] else (DIR_BLACK if piece in [BLACK] else DIR_WHITE)
        for dr, dc in directions:
            r1, c1 = r+dr, c+dc
            if 0 <= r1 < BOARD_SIZE and 0 <= c1 < BOARD_SIZE and self.board[r1][c1] == EMPTY:
                moves.append([(r,c),(r1,c1)])
        return moves

    def _dfs_capture(self, r, c, piece, path, moves, visited):
        directions = DIR_KING if piece in [BLACK_KING, WHITE_KING] else (DIR_BLACK if piece in [BLACK] else DIR_WHITE)
        any_capture = False
        for dr, dc in directions:
            r1, c1 = r+dr, c+dc
            r2, c2 = r+2*dr, c+2*dc
            if 0 <= r2 < BOARD_SIZE and 0 <= c2 < BOARD_SIZE and self.board[r2][c2] == EMPTY:
                target = self.board[r1][c1]
                if piece in [BLACK, BLACK_KING]:
                    enemy = [WHITE, WHITE_KING]
                else:
                    enemy = [BLACK, BLACK_KING]
                if target in enemy and ((r2,c2) not in visited):
                    visited.add((r2,c2))
                    self._dfs_capture(r2, c2, piece, path+[(r2,c2)], moves, visited)
                    visited.remove((r2,c2))
                    any_capture = True
        if not any_capture and len(path) > 1:
            moves.append(path)
    def is_terminal(self):
        black_pieces = sum(self.board[r][c] in [BLACK, BLACK_KING] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
        white_pieces = sum(self.board[r][c] in [WHITE, WHITE_KING] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
        if black_pieces == 0 or white_pieces == 0:
            return True
        if not self.get_legal_moves(BLACK_PLAYER) and not self.get_legal_moves(WHITE_PLAYER):
            return True
        return False

# Heuristics
def evaluate_simple(board):
    black = sum(board.board[r][c] in [BLACK, BLACK_KING] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
    white = sum(board.board[r][c] in [WHITE, WHITE_KING] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
    black_k = sum(board.board[r][c] == BLACK_KING for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
    white_k = sum(board.board[r][c] == WHITE_KING for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
    return (black + 3*black_k) - (white + 3*white_k)

def evaluate_advanced(board):
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board.board[r][c]
            if p == BLACK:
                score += 1 + r*0.1
            elif p == WHITE:
                score -= 1 + (5-r)*0.1
            elif p == BLACK_KING:
                score += 3
            elif p == WHITE_KING:
                score -= 3
    score += 0.1*(len(board.get_legal_moves(BLACK_PLAYER)) - len(board.get_legal_moves(WHITE_PLAYER)))
    return score
# Minimax + Alpha-Beta
def minimax(board, depth, maximizing, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or board.is_terminal():
        return evaluate_advanced(board), None
    player = BLACK_PLAYER if maximizing else WHITE_PLAYER
    moves = board.get_legal_moves(player)
    if not moves:
        return evaluate_advanced(board), None
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for m in moves:
            new_board = board.copy()
            new_board.apply_move(m)
            eval_score, _ = minimax(new_board, depth-1, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = m
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for m in moves:
            new_board = board.copy()
            new_board.apply_move(m)
            eval_score, _ = minimax(new_board, depth-1, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = m
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move
# Agents
class HumanAgent:
    def __init__(self, player=BLACK_PLAYER):
        self.player = player
    def get_move(self, board):
        moves = board.get_legal_moves(self.player)
        if not moves:
            return None
        for i, m in enumerate(moves):
            print(f"{i}: {m}")
        choice = int(input("Choose your move: "))
        return moves[choice]

class AI_Agent:
    def __init__(self, depth=3, maximizing=True):
        self.depth = depth
        self.maximizing = maximizing
    def get_move(self, board):
        _, move = minimax(board, self.depth, self.maximizing)
        return move

# Game loops
def play_human_vs_agent():
    board = Board()
    human = HumanAgent(BLACK_PLAYER)
    ai = AI_Agent(depth=3, maximizing=False)
    turn = BLACK_PLAYER
    while not board.is_terminal():
        board.print_board()
        if turn == BLACK_PLAYER:
            move = human.get_move(board)
        else:
            move = ai.get_move(board)
        if move is None:
            print(f"{turn} has no moves!")
            break
        board.apply_move(move)
        turn = WHITE_PLAYER if turn == BLACK_PLAYER else BLACK_PLAYER
    board.print_board()
    print("Game Over!")

def play_agent_vs_agent():
    board = Board()
    ai1 = AI_Agent(depth=3, maximizing=True)
    ai2 = AI_Agent(depth=3, maximizing=False)
    turn = BLACK_PLAYER
    while not board.is_terminal():
        board.print_board()
        if turn == BLACK_PLAYER:
            move = ai1.get_move(board)
        else:
            move = ai2.get_move(board)
        if move is None:
            break
        board.apply_move(move)
        turn = WHITE_PLAYER if turn == BLACK_PLAYER else BLACK_PLAYER
    board.print_board()
    print("Game Over!")

# Main
if __name__ == "__main__":
    mode = input("Select mode: 1. Human vs Agent  2. Agent vs Agent\n")
    if mode == "1":
        play_human_vs_agent()
    elif mode == "2":
        play_agent_vs_agent()






