import math

#board

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    return [player, player, player] in win_conditions

def is_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def get_empty_positions(board):
    positions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                positions.append((i, j))
    return positions


# minmax algo: to calculate best move for ai

def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (i, j) in get_empty_positions(board):
            board[i][j] = "O"
            score = minimax(board, depth + 1, False)
            board[i][j] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (i, j) in get_empty_positions(board):
            board[i][j] = "X"
            score = minimax(board, depth + 1, True)
            board[i][j] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for (i, j) in get_empty_positions(board):
        board[i][j] = "O"
        score = minimax(board, 0, False)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            move = (i, j)
    return move


# handling human ans ai moves

def human_move(board):
    while True:
        row = int(input("Enter the row (0, 1, or 2): "))
        col = int(input("Enter the column (0, 1, or 2): "))
        if board[row][col] == " ":
            board[row][col] = "X"
            break
        else:
            print("That position is already taken. Try again.")

def ai_move(board):
    move = best_move(board)
    if move:
        board[move[0]][move[1]] = "O"

# game loop
def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    
    while True:
        # Human move
        human_move(board)
        print_board(board)
        if check_winner(board, "X"):
            print("Congratulations, you win!")
            break
        if is_full(board):
            print("It's a tie!")
            break

        # AI move
        ai_move(board)
        print_board(board)
        if check_winner(board, "O"):
            print("AI wins! Better luck next time.")
            break
        if is_full(board):
            print("It's a tie!")
            break

# Start the game
play_game()

