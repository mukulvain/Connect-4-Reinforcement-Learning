import tkinter as tk

class ConnectFour(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect Four")
        self.geometry("700x600")
        self.board = [[0] * 7 for _ in range(6)]
        self.turn = 1  # Player 1 starts
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=700, height=600, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.drop_piece)
        self.draw_board()

    def draw_board(self):
        for col in range(7):
            for row in range(6):
                x0 = col * 100
                y0 = row * 100
                x1 = x0 + 100
                y1 = y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

    def drop_piece(self, event):
        col = event.x // 100
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.turn
                color = "brown1" if self.turn == 1 else "deep sky blue"
                self.canvas.create_oval(col * 100 + 10, row * 100 + 10, col * 100 + 90, row * 100 + 90, fill=color)
                self.turn = 3 - self.turn  # Switch player
                self.check_win()
                break

    def check_win(self):
        for row in range(6):
            for col in range(4):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3]:
                    self.game_over(self.board[row][col])

        for row in range(3):
            for col in range(7):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col]:
                    self.game_over(self.board[row][col])

        for row in range(3):
            for col in range(4):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                    self.game_over(self.board[row][col])

        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
                    self.game_over(self.board[row][col])

    def game_over(self, winner):
        if winner == 1:
            color = "red"
            message = "Player 1 wins!"
        else:
            color = "blue"
            message = "Player 2 wins!"
        self.canvas.create_text(350, 50, text=message, font=("Helvetica", 24), fill=color)
        self.canvas.unbind("<Button-1>")

if __name__ == "__main__":
    game = ConnectFour()
    game.mainloop()
