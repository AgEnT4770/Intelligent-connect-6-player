class AI_Player:
    def __init__(self, color, imp_algorithm):
        """
        color: لون الذكاء الاصطناعي (1 أسود أو 2 أبيض)
        imp_algorithm: كائن من كلاس Imp (Minimax + AlphaBeta + Heuristics)
        """
        self.color = color
        self.imp = imp_algorithm

    def make_move(self, board, depth=3, use_alpha_beta=False):
        """
        يجعل الذكاء الاصطناعي يتخذ أفضل حركة متاحة.
        
        board: كائن اللوحة
        depth: عمق البحث في Minimax
        use_alpha_beta: استخدام Minimax + AlphaBeta أو Minimax العادي
        """

        # 1) الحصول على كل الحركات المتاحة قبل اللعب
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None  # لا توجد حركات

        # ---------------------------------------------------------
        # خيار 1: استخدام Minimax مع Alpha-Beta Pruning
        # ---------------------------------------------------------
        if use_alpha_beta:
            best_score = float('-inf')
            best_move = None

            for move in valid_moves:
                row, col = move

                # محاكاة وضع الحجر
                board.place_stone(row, col, self.color)

                # تقييم الحركة باستخدام Alpha-Beta
                score = self.imp.minimax_alpha_beta(
                    board, depth - 1,
                    alpha=float('-inf'),
                    beta=float('inf'),
                    maximizing=False,
                    ai_color=self.color
                )

                # إلغاء المحاكاة
                board.remove_stone(row, col)

                # تحديث أفضل حركة
                if score > best_score:
                    best_score = score
                    best_move = move

            # تطبيق الحركة النهائية
            row, col = best_move
            board.place_stone(row, col, self.color)
            return best_move

        # ---------------------------------------------------------
        # خيار 2: استخدام Minimax العادي عبر choose_move
        # ---------------------------------------------------------
        else:
            best_move = self.imp.choose_move(
                board, depth,
                maximizing_player=True,
                color=self.color
            )

            row, col = best_move
            board.place_stone(row, col, self.color)
            return best_move
