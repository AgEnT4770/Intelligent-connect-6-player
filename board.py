# board.py

class Board:
    EMPTY = 0

    def __init__(self, size=19, win_k=6):
        self.size = size
        self.win_k = win_k
        self.grid = [[Board.EMPTY for _ in range(size)] for _ in range(size)]

    def inside(self, r, c):
        """Check if coordinates are inside the board."""
        return 0 <= r < self.size and 0 <= c < self.size

    def apply_move(self, move_combo, player):
        """
        Apply a move (one or two stones).
        Normalize move_combo into a list of (r, c) tuples.
        """
        # If it's a single tuple like (r, c), wrap it
        if isinstance(move_combo, tuple) and isinstance(move_combo[0], int):
            move_combo = [move_combo]

        # If it's a list but contains a nested tuple, flatten it
        if isinstance(move_combo, list) and len(move_combo) == 1 and isinstance(move_combo[0], tuple):
            inner = move_combo[0]
            if isinstance(inner[0], tuple):  # e.g. [((r, c))]
                move_combo = [inner[0]]

        for (r, c) in move_combo:
            if not self.inside(r, c) or self.grid[r][c] != Board.EMPTY:
                raise ValueError(f"Invalid move at ({r}, {c})")
            self.grid[r][c] = player

    def undo_move(self, move_combo):
        """
        Undo a move (remove one or two stones).
        Normalize move_combo into a list of (r, c) tuples.
        """
        if isinstance(move_combo, tuple) and isinstance(move_combo[0], int):
            move_combo = [move_combo]

        if isinstance(move_combo, list) and len(move_combo) == 1 and isinstance(move_combo[0], tuple):
            inner = move_combo[0]
            if isinstance(inner[0], tuple):  # e.g. [((r, c))]
                move_combo = [inner[0]]

        for (r, c) in move_combo:
            if self.inside(r, c):
                self.grid[r][c] = Board.EMPTY

    def check_win(self, player):
        """Check if the given player has a winning line of length win_k."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != player:
                    continue
                for dr, dc in directions:
                    count = 1
                    nr, nc = r + dr, c + dc
                    while self.inside(nr, nc) and self.grid[nr][nc] == player:
                        count += 1
                        if count >= self.win_k:
                            return True
                        nr += dr
                        nc += dc
        return False

    def check_draw(self):
        """Check if the board is full (draw)."""
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == Board.EMPTY:
                    return False
        return True

    def reset(self):
        """Reset the board to empty state."""
        self.grid = [[Board.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def copy(self):
        """Return a deep copy of the board for search algorithms."""
        new_board = Board(size=self.size, win_k=self.win_k)
        new_board.grid = [row[:] for row in self.grid]
        return new_board

    def __str__(self):
        """String representation for debugging."""
        rows = []
        for r in range(self.size):
            row = " ".join(str(self.grid[r][c]) for c in range(self.size))
            rows.append(row)
        return "\n".join(rows)
