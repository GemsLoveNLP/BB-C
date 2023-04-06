import numpy as np

class slot:
    def __init__(self, piece='d'):
        self.piece = piece  

    def change_piece(self, new_piece):
        self.piece = new_piece

def board(board_size=4):
    board = []
    for i in range(board_size):
        board.append([slot() for i in range(board_size)])
    return board

class board:
    def __init__(self):
        self.board = board()
    
    def set_piece(self, row, col, piece):
        self.board[row][col].change_piece(piece)



