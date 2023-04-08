orientation_list = [ [[1,0],[0,1]], [[0,1],[-1,0]], [[-1,0],[0,-1]], [[0,-1],[1,0]] ] 
shift_dict = { "L": [[0,0], [0,1], [1,1], [1,0]], "D": [[0,0], [2,0], [1,-1], [0,-1]]}

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
    def __init__(self, piece, height, width, tall, orientation, holes=[]):
        self.piece = piece
        self.height = height
        self.width = width
        self.tall = tall
        self.holes = holes #list of holes, each hole is a list of [y,x]
        self.orientation = orientation #num of possible oreintation

    def area(self):
        return self.height*self.width
    
def setup():
    # pieces
    global L, T, I, F
    L = block("L",2,2,2,4,[[1,0]])
    T = block("T",2,3,2,4,[[0,1],[2,1]])
    I = block("I",2,1,2,2,[])
    F = block("F",2,2,2,1,[])
    #  constants
    global threshold
    threshold = 100

class slot:
    def __init__(self, piece=' '):
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


class game_board:
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
                if row+y>=self.size or col+x>=self.size:
                    return False
                else:
                    if (row+y, col+x) not in true_hole:
                        if self.board[row+y][col+x].piece != ' ':
                            return False
        return True

    def place_block(self, height, width, row, col, piece, hole=[]):
        true_hole = [(i+row, j+col) for i,j in hole]
        for y in range(height):
            for x in range(width):
                if (row+y, col+x) not in true_hole and row+y<self.size and col+x<self.size:
                    self.set_piece(row+y,col+x,piece)

    def randomize(self, piece: block, debug):
        r = rd.randint(0,self.size)
        c = rd.randint(0,self.size)
        o = rd.randint(0,piece.orientation-1)
        holes = []
        for old_hole in piece.holes:
            holes.append(transform_hole(old_hole, o, piece.piece))
        if self.check_fit(piece.height, piece.width, r, c, holes):
            self.place_block(piece.height, piece.width, r, c, piece.piece, holes)
            if debug:
                print(f"randomize() --> success (r,c,o) = ({r},{c},{o})")
            return True
        else:
            if debug:
                print(f"randomize() --> Failed (r,c,o) = ({r},{c},{o})")
            return False

    def randomize_pieces(self, pieces, debug=False):
        new_list = sorted([[piece.area()-len(piece.holes), piece.piece, piece] for piece in pieces], reverse=True)
        for area, name, piece in new_list:
            for i in range(threshold):
                if self.randomize(piece,debug):
                    if debug:
                        print(f"randomize_pieces --> success {piece.piece}")
                    break  
                 