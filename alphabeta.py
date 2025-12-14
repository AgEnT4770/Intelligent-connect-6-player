# alphabeta.py

import time
from itertools import combinations
from heuristics import longest_chain_open

class AlphaBeta:
    def __init__(self,
                 max_depth,
                 heuristic_func,
                 stones_per_move=2,
                 win_k=6,
                 near_radius=2,
                 iterative_deepening=True,
                 time_limit_sec=2.0):
        self.max_depth = max_depth
        self.heuristic_func = heuristic_func
        self.stones_per_move = stones_per_move
        self.win_k = win_k
        self.near_radius = near_radius
        self.iterative_deepening = iterative_deepening
        self.time_limit_sec = time_limit_sec

    def _is_near_stone(self, board_grid, r, c, radius=None):
        if radius is None:
            radius = self.near_radius
        N = len(board_grid)
        for dr in range(-radius, radius+1):
            for dc in range(-radius, radius+1):
                nr, nc = r+dr, c+dc
                if 0 <= nr < N and 0 <= nc < N and board_grid[nr][nc] != 0:
                    return True
        return False

    def _creates_block(self, board_grid, move, opp_player):
        r, c = move
        board_grid[r][c] = opp_player
        length, open_ends = longest_chain_open(board_grid, opp_player)
        board_grid[r][c] = 0
        return length >= self.win_k - 1 and open_ends > 0

    def get_moves(self, board_grid, opp_player=None):
        N = len(board_grid)
        moves = []
        any_stone = any(board_grid[r][c] != 0 for r in range(N) for c in range(N))
        for r in range(N):
            for c in range(N):
                if board_grid[r][c] == 0:
                    if not any_stone or self._is_near_stone(board_grid, r, c):
                        moves.append((r, c))
        center_r, center_c = N // 2, N // 2
        if opp_player is not None:
            moves.sort(key=lambda m: (
                0 if self._creates_block(board_grid, m, opp_player) else 1,
                abs(m[0]-center_r) + abs(m[1]-center_c)
            ))
        else:
            moves.sort(key=lambda m: abs(m[0]-center_r) + abs(m[1]-center_c))
        return moves

    def evaluate_terminal(self, board_obj, my_player, opp_player, depth):
        if board_obj.check_win(my_player):
            return float('inf') - depth
        if board_obj.check_win(opp_player):
            return float('-inf') + depth
        moves = self.get_moves(board_obj.grid, opp_player)
        if depth >= self.max_depth or not moves:
            return self.heuristic_func(board_obj.grid, my_player, opp_player,
                                       win_k=self.win_k, depth=depth)
        return None

    def alphabeta(self, board_obj, depth, alpha, beta, is_maximizing, my_player, opp_player, deadline):
        if time.time() >= deadline:
            return [], self.heuristic_func(board_obj.grid, my_player, opp_player,
                                           win_k=self.win_k, depth=depth)
        term = self.evaluate_terminal(board_obj, my_player, opp_player, depth)
        if term is not None:
            return [], term
        moves = self.get_moves(board_obj.grid, opp_player)
        k = min(self.stones_per_move, len(moves))
        move_combinations = list(combinations(moves, k)) if k > 0 else []
        if is_maximizing:
            best_score = float('-inf')
            best_move = []
            for combo in move_combinations:
                if time.time() >= deadline: break
                board_obj.apply_move(combo, my_player)
                _, score = self.alphabeta(board_obj, depth+1, alpha, beta, False, my_player, opp_player, deadline)
                board_obj.undo_move(combo)
                if score is not None and score > best_score:
                    best_score, best_move = score, list(combo)
                alpha = max(alpha, best_score)
                if beta <= alpha: break
            return best_move, best_score
        else:
            best_score = float('inf')
            best_move = []
            for combo in move_combinations:
                if time.time() >= deadline: break
                board_obj.apply_move(combo, opp_player)
                _, score = self.alphabeta(board_obj, depth+1, alpha, beta, True, my_player, opp_player, deadline)
                board_obj.undo_move(combo)
                if score is not None and score < best_score:
                    best_score, best_move = score, list(combo)
                beta = min(beta, best_score)
                if beta <= alpha: break
            return best_move, best_score

    def choose_move(self, board_obj, my_player, opp_player):
        deadline = time.time() + max(0.2, float(self.time_limit_sec))
        best_move, best_score = [], None
        if not self.iterative_deepening:
            return self.alphabeta(board_obj.copy(), 0, float('-inf'), float('inf'),
                                  True, my_player, opp_player, deadline)
        original_max = self.max_depth
        for d in range(1, original_max+1):
            if time.time() >= deadline: break
            self.max_depth = d
            move, score = self.alphabeta(board_obj.copy(), 0, float('-inf'), float('inf'),
                                         True, my_player, opp_player, deadline)
            if move: best_move, best_score = move, score
        self.max_depth = original_max
        return best_move, best_score