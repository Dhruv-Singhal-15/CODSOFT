import tkinter as tk
import math

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


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.current_player = "X"
        self.game_over = False
        self.message_box = None  

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=("Arial", 20), width=10, height=6,
                                   command=lambda i=i, j=j: self.human_move(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def human_move(self, i, j):
        if self.board[i][j] == " " and not self.game_over:
            self.board[i][j] = "X"
            self.buttons[i][j].config(text="X")
            if check_winner(self.board, "X"):
                self.show_message("Congratulations, you win! Play again?")
            elif is_full(self.board):
                self.show_message("It's a tie! Play again?")
            else:
                self.ai_move()

    def ai_move(self):
        move = best_move(self.board)
        if move:
            self.board[move[0]][move[1]] = "O"
            self.buttons[move[0]][move[1]].config(text="O")
            if check_winner(self.board, "O"):
                self.show_message("AI wins! Play again?")
            elif is_full(self.board):
                self.show_message("It's a tie! Play again?")

    def show_message(self, message):
        if self.message_box:
            self.message_box.destroy() 

        self.message_box = tk.Toplevel(self.root)
        self.message_box.title("Game Over")
        self.message_box.geometry("250x150")
        message_label = tk.Label(self.message_box, text=message, font=("Arial", 14))
        message_label.pack(pady=20, padx=10)
        
        button_frame = tk.Frame(self.message_box)
        button_frame.pack(pady=10)

        play_again_button = tk.Button(button_frame, text="Play Again", command=self.restart_game)
        play_again_button.grid(row=0, column=0, padx=10)

        quit_button = tk.Button(button_frame, text="Quit", command=self.root.destroy)
        quit_button.grid(row=0, column=1, padx=10)

    def restart_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")
        self.game_over = False
        self.message_box.destroy() 


def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
