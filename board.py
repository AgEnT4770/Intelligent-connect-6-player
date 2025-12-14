class Board:
    EMPTY = 0

    def __init__(self, size=19, win_k=6):
        """
        size  : حجم اللوحة (n x n)
        win_k : عدد الأحجار المطلوبة للفوز (Connect-6)
        """
        self.size = size
        self.win_k = win_k
        self.grid = [[Board.EMPTY for _ in range(size)] for _ in range(size)]

    # ======================
    # Basic helpers
    # ======================
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

    # ======================
    # Moves
    # ======================
    def get_valid_moves(self):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == Board.EMPTY:
                    moves.append((r, c))
        return moves

    def apply_move(self, move_combo, player):
        """
        move_combo : tuple[(r,c), ...]  (حجرتين في Connect-6)
        """
        for (r, c) in move_combo:
            if not self.inside(r, c) or self.grid[r][c] != Board.EMPTY:
                raise ValueError("Invalid move")
            self.grid[r][c] = player

    def undo_move(self, move_combo):
        for (r, c) in move_combo:
            self.grid[r][c] = Board.EMPTY

    # ======================
    # Win checking
    # ======================
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
        return all(self.grid[r][c] != Board.EMPTY
                   for r in range(self.size)
                   for c in range(self.size))

    # ======================
    # Display (UI / Debug)
    # ======================
    def display(self):
        print("   " + " ".join(f"{i:2}" for i in range(self.size)))
        for r in range(self.size):
            row = []
            for c in range(self.size):
                val = self.grid[r][c]
                if val == 0:
                    row.append(".")
                elif val == 1:
                    row.append("X")
                else:
                    row.append("O")
            print(f"{r:2} " + " ".join(row))
