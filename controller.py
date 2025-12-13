class HumanPlayer:
    def __init__(self, color):
        self.color = color

class GameController:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.game_over = False
        self.winner = None

    # switch turns function
    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


    # core function
    def play_move(self, move_combo):
        """
        move_combo: tuple[(r,c), (r,c)]
        """
        if self.game_over:      # base case to end the game
            return

        player_color = self.current_player.color
        self.board.apply_move(move_combo, player_color)

        if self.board.check_win(player_color):
            self.game_over = True
            self.winner = self.current_player
            return

        if self.board.is_full():        # draw case (Full board with no winner)
            self.game_over = True
            self.winner = None
            return

        self.switch_player()


    # AI move
    def ai_move(self):
        if self.game_over:
            return None

        # اتأكد إن current_player عنده make_move (يعني AI)
        if not hasattr(self.current_player, "make_move"):
            return None  # مش AI، يبقى human

        # مرر Board object كامل للـ AI
        move = self.current_player.make_move(self.board)

        if move:
            # لو الحركة خلت AI يكسب
            if self.board.check_win(self.current_player.color):
                self.game_over = True
                self.winner = self.current_player
            else:
                # لو مش كسب، نبدل الدور
                self.switch_player()

        return move




