# gui.py

import tkinter as tk
from tkinter import messagebox
import threading

from board import Board
from controller import GameController, HumanPlayer
from Ai_Player import AI_Player
from minimax import Minimax
from alphabeta import AlphaBeta
from heuristics import heuristic1, heuristic2

class Connect6GUI:
    def __init__(self, master):
        self.master = master
        master.title("Connect 6")

        self.board_size = tk.IntVar(value=19)
        self.ai_depth = tk.IntVar(value=2)  # Lower default for responsiveness
        self.ai_heuristic = tk.StringVar(value="heuristic2")  # Heuristic2 tends to be stronger
        self.ai_algo = tk.StringVar(value="AlphaBeta")

        self.board = None
        self.controller = None

        self.cell_size = 30
        self.board_padding = 5
        self.first_stone_pos = None

        # Prevent double AI runs
        self._ai_running = False

        self.create_setup_frame()

    def create_setup_frame(self):
        self.setup_frame = tk.Frame(self.master)
        self.setup_frame.pack(padx=10, pady=10)

        tk.Label(self.setup_frame, text="Board Size (N x N):").grid(row=0, column=0, sticky="w")
        tk.Entry(self.setup_frame, textvariable=self.board_size).grid(row=0, column=1, sticky="ew")

        tk.Label(self.setup_frame, text="AI Depth:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.setup_frame, textvariable=self.ai_depth).grid(row=1, column=1, sticky="ew")

        tk.Label(self.setup_frame, text="AI Heuristic:").grid(row=2, column=0, sticky="w")
        tk.OptionMenu(self.setup_frame, self.ai_heuristic, "heuristic1", "heuristic2").grid(row=2, column=1, sticky="ew")

        tk.Label(self.setup_frame, text="Algorithm:").grid(row=3, column=0, sticky="w")
        tk.OptionMenu(self.setup_frame, self.ai_algo, "AlphaBeta", "Minimax").grid(row=3, column=1, sticky="ew")

        tk.Button(self.setup_frame, text="Start Game", command=self.start_game).grid(row=4, column=0, columnspan=2, pady=8)

    def start_game(self):
        try:
            size = self.board_size.get()
            depth = self.ai_depth.get()
            heuristic_name = self.ai_heuristic.get()
            algo_name = self.ai_algo.get()

            if size < 6:
                messagebox.showerror("Error", "Board size must be at least 6 for Connect 6.")
                return

            heuristic_func = heuristic1 if heuristic_name == "heuristic1" else heuristic2
            self.board = Board(size=size)

            human_player = HumanPlayer(1)
            if algo_name == "AlphaBeta":
                ai_algorithm = AlphaBeta(
                    max_depth=depth,
                    heuristic_func=heuristic_func,
                    win_k=self.board.win_k,
                    near_radius=2,
                    iterative_deepening=True,
                    time_limit_sec=5.0
                )
            else:
                ai_algorithm = Minimax(
                    max_depth=depth,
                    heuristic_func=heuristic_func,
                    win_k=self.board.win_k,
                    near_radius=2,
                    iterative_deepening=True,
                    time_limit_sec=5.0
                )
            ai_player = AI_Player(2, ai_algorithm)

            self.controller = GameController(self.board, human_player, ai_player, first_move_single=True)

            # Dynamic scaling
            self.cell_size = max(16, min(40, 700 // self.board.size))

            self.setup_frame.destroy()
            self.create_game_board_frame()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Board Size and AI Depth.")

    def create_game_board_frame(self):
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=10, pady=10)

        width = self.board.size * self.cell_size + self.board_padding
        height = self.board.size * self.cell_size + self.board_padding

        self.canvas = tk.Canvas(self.game_frame, width=width, height=height, bg="#D2B48C")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.status_label = tk.Label(self.game_frame, text="")
        self.status_label.pack(pady=6)

        self.restart_btn = tk.Button(self.game_frame, text="Restart", command=self.restart_game)
        self.restart_btn.pack(pady=4)

        self.draw_board()
        self.update_status()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.board.size):
            for c in range(self.board.size):
                x1 = c * self.cell_size + self.board_padding
                y1 = r * self.cell_size + self.board_padding
                x2 = (c + 1) * self.cell_size + self.board_padding
                y2 = (r + 1) * self.cell_size + self.board_padding
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="#F5DEB3")

                player = self.board.grid[r][c]
                if player == 1:
                    self.canvas.create_oval(x1 + 4, y1 + 4, x2 - 4, y2 - 4, fill="red", outline="red")
                elif player == 2:
                    self.canvas.create_oval(x1 + 4, y1 + 4, x2 - 4, y2 - 4, fill="blue", outline="blue")

        if self.first_stone_pos is not None:
            r, c = self.first_stone_pos
            x1 = c * self.cell_size + self.board_padding
            y1 = r * self.cell_size + self.board_padding
            x2 = (c + 1) * self.cell_size + self.board_padding
            y2 = (r + 1) * self.cell_size + self.board_padding
            self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, outline="green", width=2)

    def handle_click(self, event):
        if self.controller.game_over or self._ai_running:
            return

        from Ai_Player import AI_Player as AIClass
        if isinstance(self.controller.current_player, AIClass):
            messagebox.showinfo("Turn", "It's the AI's turn!")
            return

        c = (event.x - self.board_padding) // self.cell_size
        r = (event.y - self.board_padding) // self.cell_size

        if not (0 <= r < self.board.size and 0 <= c < self.board.size) or self.board.grid[r][c] != Board.EMPTY:
            messagebox.showwarning("Invalid Move", "Please select an empty cell within the board.")
            return

        # First move: only one stone
        if self.controller._moves_played == 0:
            move_combo = [(r, c)]
            res = self.controller.play_move(move_combo)
            if res is None:
                messagebox.showerror("Invalid Move", "Move rejected.")
            else:
                self.draw_board()
                self.update_status()
                if not self.controller.game_over and isinstance(self.controller.current_player, AIClass):
                    self.run_ai_in_background()
            return

        # Subsequent moves: two stones
        if self.first_stone_pos is None:
            self.first_stone_pos = (r, c)
            self.update_status(extra="First stone selected. Place your second stone.")
            self.draw_board()
            return
        second_stone_pos = (r, c)
        if second_stone_pos == self.first_stone_pos:
            messagebox.showwarning("Invalid Move", "Second stone must be in a different cell.")
            return

        move_combo = [self.first_stone_pos, second_stone_pos]
        res = self.controller.play_move(move_combo)
        self.first_stone_pos = None

        if res is None:
            messagebox.showerror("Invalid Move", "Move rejected.")
        else:
            self.draw_board()
            self.update_status()
            if not self.controller.game_over and isinstance(self.controller.current_player, AIClass):
                self.run_ai_in_background()
        if self.controller.game_over or self._ai_running:
            return

        from Ai_Player import AI_Player as AIClass
        if isinstance(self.controller.current_player, AIClass):
            messagebox.showinfo("Turn", "It's the AI's turn!")
            return

        c = (event.x - self.board_padding) // self.cell_size
        r = (event.y - self.board_padding) // self.cell_size

        if not (0 <= r < self.board.size and 0 <= c < self.board.size) or self.board.grid[r][c] != Board.EMPTY:
            messagebox.showwarning("Invalid Move", "Please select an empty cell within the board.")
            return

        if self.first_stone_pos is None:
            self.first_stone_pos = (r, c)
            self.update_status(extra="First stone selected. Place your second stone.")
            self.draw_board()
            return

        second_stone_pos = (r, c)
        if second_stone_pos == self.first_stone_pos:
            messagebox.showwarning("Invalid Move", "Second stone must be in a different cell.")
            return

        move_combo = (self.first_stone_pos, second_stone_pos)
        res = self.controller.play_move(move_combo)
        self.first_stone_pos = None

        if res is None:
            messagebox.showerror("Invalid Move", "Move rejected.")
        else:
            self.draw_board()
            self.update_status()

            # If AI turn and game not over, run AI on a background thread
            if not self.controller.game_over and isinstance(self.controller.current_player, AIClass):
                self.run_ai_in_background()

    def run_ai_in_background(self):
        if self._ai_running:
            return
        self._ai_running = True
        self.update_status(extra="AI thinking...")

        def ai_task():
            move, score = self.controller.ai_move()
            # Schedule GUI updates safely on the main thread
            self.master.after(0, lambda: self.after_ai_move(move, score))

        t = threading.Thread(target=ai_task, daemon=True)
        t.start()

    def after_ai_move(self, move, score):
        self._ai_running = False
        if move:
            self.draw_board()
            self.update_status(extra=f"AI evaluated: {score:.2f}" if score is not None else None)
        else:
            messagebox.showerror("AI Error", "AI could not make a move.")
            self.controller.game_over = True
            self.update_status(extra="AI failed to move. Game ended.")

    def update_status(self, extra=None):
        if self.controller.game_over:
            if self.controller.winner:
                winner_color = "Red" if self.controller.winner.color == 1 else "Blue"
                self.status_label.config(text=f"Game Over! Winner: {winner_color}")
            else:
                self.status_label.config(text="Game Over! It's a Draw.")
        else:
            current_player_color = "Red" if self.controller.current_player.color == 1 else "Blue"
            from controller import HumanPlayer
            player_type = "(Human)" if isinstance(self.controller.current_player, HumanPlayer) else "(AI)"
            base = f"Current Turn: {current_player_color} {player_type}"
            if extra:
                base += f" — {extra}"
            self.status_label.config(text=base)

    def restart_game(self):
        if hasattr(self, 'game_frame'):
            self.game_frame.destroy()
        self.first_stone_pos = None
        self.board = None
        self.controller = None
        self._ai_running = False
        self.create_setup_frame()

def main():
    root = tk.Tk()
    gui = Connect6GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()