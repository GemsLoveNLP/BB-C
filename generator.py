import numpy as np
import random as rd
import math

# ? Note: key is in top left, one key piece in block

orientation_list = [ [[1,0],[0,1]], [[0,1],[-1,0]], [[-1,0],[0,-1]], [[0,-1],[1,0]] ] 
shift_dict = { "L": [[0,0], [1,0], [1,-1], [0,-1]], "R": [[0,0], [2,0], [1,-1], [0,-1]]}

def transform_hole(hole, orientation, piece):    
    matrix = np.array(orientation_list[orientation])
    vector = np.array(list(hole))
    rotated = np.matmul(matrix, vector)
    shift_array = np.array(shift_dict[piece][orientation])
    return list(rotated + shift_array)

def draw(l):
    size = len(l)
    s = ""
    s+="-"*(4*size+1)
    s+="\n"
    for i in range(size):
        s+="|"
        for j in range(size):
            s+=" "
            s+=str(l[i][j])
            s+=" |"
        s+="\n"
        s+="-"*(4*size+1)
        s+="\n"
    return s

class block:
    def __init__(self, piece, height, width, tall, holes=[], orientation=0):
        self.piece = piece
        self.height = height
        self.width = width
        self.tall = tall
        self.holes = holes
        self.orientation = orientation

    def area(self):
        return self.height*self.width
    
def setup():
    global L
    L = block("L",2,2,2,[[1,0]],0)

class slot:
    def __init__(self, piece='d'):
        self.piece = piece  

    def change_piece(self, new_piece):
        self.piece = new_piece

def generate_board(board_size):
    board_ = []
    for i in range(board_size):
        board_.append([slot() for i in range(board_size)])
    return board_

def transform(array):
    l = []
    for i in array:
        temp = []
        for j in i:
            temp.append(slot(j))
        l.append(temp)
    return np.array(l)

class board:
    def __init__(self, auto=True, array=np.array([]), size=4):
        if not auto:
            self.board = transform(array)
        else:
            self.board = generate_board(size)
        self.size=size

    def __str__(self):
        view = []
        for row in self.board:
            temp = []
            for obj in row:
                temp.append(obj.piece)
            view.append(temp)
        return draw(view)
    
    def clear(self):
        self.board = generate_board(self.size)
    
    def set_piece(self, row, col, piece):
        self.board[row][col].change_piece(piece)

    def check_fit(self, height, width, row, col, hole=[]):
        true_hole = [(i+row, j+col) for i,j in hole]
        for y in range(height):
            for x in range(width):
                if (row+y, row+x) not in true_hole:
                    if board[row+y][col+x].piece != 'd':
                        return False
        return True

    def place_block(self, height, width, row, col, piece, hole=[]):
        true_hole = [(i+row, j+col) for i,j in hole]
        for y in range(height):
            for x in range(width):
                if (row+y, row+x) not in true_hole:
                    self.set_piece(row+y,col+x,piece)