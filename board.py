# board.py

class Board:
    EMPTY = 0

    def __init__(self, size=19, win_k=6):
        self.size = size
        self.win_k = win_k
        self.grid = [[Board.EMPTY for _ in range(size)] for _ in range(size)]

    def reset(self):
        self.grid = [[Board.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def copy(self):
        new_board = Board(self.size, self.win_k)
        for r in range(self.size):
            for c in range(self.size):
                new_board.grid[r][c] = self.grid[r][c]
        return new_board

    def inside(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def get_valid_moves(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == Board.EMPTY]

    def apply_move(self, move_combo, player):
        if isinstance(move_combo, tuple) and isinstance(move_combo[0], int):
            move_combo = [move_combo]
        for (r, c) in move_combo:
            if not self.inside(r, c) or self.grid[r][c] != Board.EMPTY:
                raise ValueError(f"Invalid move at ({r}, {c})")
        for (r, c) in move_combo:
            self.grid[r][c] = player

    def undo_move(self, move_combo):
        if isinstance(move_combo, tuple) and isinstance(move_combo[0], int):
            move_combo = [move_combo]
        for (r, c) in move_combo:
            if self.inside(r, c):
                self.grid[r][c] = Board.EMPTY

    def check_win(self, player):
        DIRS = [(0,1), (1,0), (1,1), (1,-1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != player:
                    continue
                for dr, dc in DIRS:
                    count = 0
                    rr, cc = r, c
                    while self.inside(rr, cc) and self.grid[rr][cc] == player:
                        count += 1
                        rr += dr
                        cc += dc
                    if count >= self.win_k:
                        return True
        return False

    def is_full(self):
        return all(self.grid[r][c] != Board.EMPTY for r in range(self.size) for c in range(self.size))

    def check_draw(self):
        return self.is_full() and not self.check_win(1) and not self.check_win(2)