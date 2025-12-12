# minimax.py

import copy
from itertools import combinations
from heuristics import heuristic1, heuristic2

def check_win(board, player, k=6):
    N = len(board)
    DIRS = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(N):
        for c in range(N):
            if board[r][c] != player:
                continue
            for dr, dc in DIRS:
                cnt = 0
                rr, cc = r, c
                while 0 <= rr < N and 0 <= cc < N and board[rr][cc] == player:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= k:
                    return True
    return False

class Minimax:
    def __init__(self, max_depth, heuristic_func, stones_per_move=2, win_k=6):
        self.max_depth = max_depth
        self.heuristic_func = heuristic_func
        self.stones_per_move = stones_per_move
        self.win_k = win_k

    def get_moves(self, board):
        N = len(board)
        moves = []
        for r in range(N):
            for c in range(N):
                if board[r][c] == 0:
                    moves.append((r,c))
        return moves

    def evaluate_terminal(self, board, my_player, opp_player, depth):
        # win checks
        if check_win(board, my_player, self.win_k):
            return float('inf')
        if check_win(board, opp_player, self.win_k):
            return float('-inf')
        # depth or no moves
        moves = self.get_moves(board)
        if depth >= self.max_depth or not moves:
            return self.heuristic_func(board, my_player, opp_player)
        return None  # not terminal

    def minimax(self, board, depth, is_maximizing, my_player, opp_player):
        term = self.evaluate_terminal(board, my_player, opp_player, depth)
        if term is not None:
            return None, term

        moves = self.get_moves(board)
        # generate combined moves: choose stones_per_move distinct empty positions
        move_combinations = list(combinations(moves, min(self.stones_per_move, len(moves))))

        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for combo in move_combinations:
                # apply combo
                for (r,c) in combo:
                    board[r][c] = my_player
                _, score = self.minimax(board, depth + 1, False, my_player, opp_player)
                # undo
                for (r,c) in combo:
                    board[r][c] = 0
                if score is not None and score > best_score:
                    best_score = score
                    best_move = combo
            return best_move, best_score
        else:
            best_score = float('inf')
            best_move = None
            for combo in move_combinations:
                for (r,c) in combo:
                    board[r][c] = opp_player
                _, score = self.minimax(board, depth + 1, True, my_player, opp_player)
                for (r,c) in combo:
                    board[r][c] = 0
                if score is not None and score < best_score:
                    best_score = score
                    best_move = combo
            return best_move, best_score

    def choose_move(self, board, my_player, opp_player):
        # returns best combo of positions to play (tuple of (r,c))
        move, score = self.minimax(board, 0, True, my_player, opp_player)
        return move, score
