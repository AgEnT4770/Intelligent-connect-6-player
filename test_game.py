from board import Board
from ai_player import AI_Player
from alphabeta import AlphaBeta
from heuristics import heuristic2
from controller import GameController, HumanPlayer

# ==== Setup ====
board = Board()
ai_algo = AlphaBeta(max_depth=1, heuristic_func=heuristic2)
ai = AI_Player(color=2, imp_algorithm=ai_algo)
human = HumanPlayer(color=1)
game = GameController(board, human, ai)

# ==== Game loop ====
while not game.game_over:
    # ---- Human move ----
    print("\nYour move:")
    move = ((int(input("r1: ")), int(input("c1: "))),
            (int(input("r2: ")), int(input("c2: "))))
    game.play_move(move)
    board.display()
    
    if game.game_over:
        break

    # ---- AI move ----
    print("\nAI is thinking...")
    game.ai_move()
    board.display()

# ==== Game over ====
print("\nGame Over!")
if game.winner:
    print("Winner:", "Human" if game.winner == human else "AI")
else:
    print("Draw!")
