#HEURISTIC 1
def count_stones(board, r, c, dr, dc, player):
    count = 0
    N = len(board)
    while 0 <= r < N and 0 <= c < N and board[r][c] == player:
        count += 1
        r += dr
        c += dc
    return count

def longest_chain_open(board, player):
    DIRS = [(0,1), (1,0), (1,1), (1,-1)] #directions: right, down, downRight diagonal, downLeft
    N = len(board)
    best_length = 0
    best_open = 0

    for r in range(N):
        for c in range(N):
            if board[r][c] != player:
                continue

            for dr, dc in DIRS:
                left  = count_stones(board, r-dr, c-dc, -dr, -dc, player)
                right = count_stones(board, r+dr, c+dc,  dr,  dc, player)
                length = left + 1 + right

                #open ends
                end1_r = r - (left + 1)*dr
                end1_c = c - (left + 1)*dc
                end2_r = r + (right + 1)*dr
                end2_c = c + (right + 1)*dc

                def is_open(rr, cc):
                    return 0 <= rr < N and 0 <= cc < N and board[rr][cc] == 0

                open_ends = is_open(end1_r, end1_c) + is_open(end2_r, end2_c)

                # use chain only if there's at least one open end
                if open_ends > 0 and length > best_length:
                    best_length = length
                    best_open = open_ends

    return best_length, best_open

def heuristic1(board, my_player, opp_player): #open ends used as weights
    my_len, my_open = longest_chain_open(board, my_player)
    opp_len, opp_open = longest_chain_open(board, opp_player)
    return my_len * my_open - opp_len * opp_open

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#HEURISTIC 2

#mobility: number of open cells adajcent to stones/valid moves
def mobility(board, player):
    N = len(board)
    moves = set()
    #using set to avoid counting the same cell twice (if two stones share a neighbor)
    for r in range(N):
        for c in range(N):
            if board[r][c] == player:
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]: #same as using DIRS with -1,-1  -1,0  -1,1,  1,0,  1,1  0,0  0,1  0,-1  1,-1
                        if dr == 0 and dc == 0:
                            continue #skipping the current position of the stone
                        nr = r + dr
                        nc = c + dc
                        #neighbor cells positions
                        if 0 <= nr < N and 0 <= nc < N and board[nr][nc] == 0:
                            moves.add((nr, nc))
    return len(moves)


#threat: longest chains with open ends (heuristic 1)
def threat(board, player):
    length, open_ends = longest_chain_open(board, player)
    return length * open_ends


#center control: how close to center:: centerWeight = - (|r - midR| + |c - midC|)
#calculate for all stones and return total center control for the player
#higher score = better : more stones in the center
def center_control(board, player):
    N = len(board)
    midR, midC = (N-1)//2, (N-1)//2 #-1 to work for both even and odd
    total = 0
    for r in range(N):
        for c in range(N):
            if board[r][c] == player:
                dist = abs(r - midR) + abs(c - midC) #manhattan distance
                total += -dist
    return total


def heuristic2(board, my_player, opp_player, A=2, B=3, C=1):
    my_mob  = mobility(board, my_player)
    opp_mob = mobility(board, opp_player)
    my_threat  = threat(board, my_player)
    opp_threat = threat(board, opp_player)
    my_center  = center_control(board, my_player)
    opp_center = center_control(board, opp_player)

    h = (A * (my_mob - opp_mob)
       + B * (my_threat - opp_threat)
       + C * (my_center - opp_center))
    return h


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#test

'''
def main():
    board = [
        [0,0,0,0,0,0],
        [0,1,1,1,0,0],
        [0,0,0,0,0,0],
        [0,2,2,0,0,2],
        [0,0,0,0,0,2],
        [0,0,0,0,0,2],
    ]

    print("Board:")
    for row in board:
        print(row)

    h1 = heuristic1(board, my_player=1, opp_player=2)
    print("\nHeuristic1 value =", h1)

    h2 = heuristic2(board, my_player=1, opp_player=2, A=2, B=3, C=1)
    print("Heuristic2 value =", h2)

if __name__ == "__main__":
    main()
'''
