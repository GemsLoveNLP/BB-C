import random as rd

# setup
GRID_SIZE = 5
COLORS = ['r','o','y','l','b','v']
COLORS_EXTENDED = ['r','o','y','l','g','b','i','v','p']
RANK_COLORS = ['goldenrod', 'silver', 'chocolate1', 'azure4'] 
INFOS = {
        'r': ['crimson', 'RED'],
        'o': ['darkorange', 'ORANGE'],
        'y': ['gold', 'YELLOW'],
        'l': ['chartreuse2','LIME'],
        'g': ['springgreen4','GREEN'],
        'b': ['steelblue2', 'BLUE'],
        'i': ['dodgerblue3','INDIGO'],
        'v': ['mediumpurple','VIOLET'],
        'p': ['palevioletred1', 'PINK']
        }
size = width, height = (800,800)

# transform hex into correct form
def hex_to_dec(HEX):
    r = int(HEX[0:2],base=16)
    g = int(HEX[2:4],base=16)
    b = int(HEX[4:6],base=16)
    return r,g,b

# randomize n color(s) from COLORS. return str(color) if n=1 else return a list of colors
def rand_color(colorful=False, n=1):   
    if colorful:
        colors = COLORS_EXTENDED
    else:
        colors = COLORS 
    copy = [color for color in colors]
    rd.shuffle(copy)
    if n == 1:
        return copy[0]
    return copy[:min(n,len(colors))]

# return a dict of the color for the text_screen. keys = 'text','text_color','background'
def text_screen_random(colorful=False):
    temp = rand_color(colorful=colorful,n=3)
    dic = dict()
    dic['text'] = temp[0]
    dic['text_color'] = temp[1]
    dic['background'] = temp[2]
    return dic

# change a n**2 long list to a nxn 2D list
def to_square_matrix(l):
    s = int(len(l)**0.5)
    a = [l[i*s:i*s+s] for i in range(s)]
    return a

# draw a 2D list
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

# class of each cell in a board
class cell:
    # color = color, status = who has their marker on represented by the player number (default=0=no one)
    def __init__(self, color, status=0):
        self.color = color
        self.status = status

# generate a color board which has at least n copy of all colors
def color_board(board_size=GRID_SIZE**2, num_players=4, copy=3, colorful=False):
    # color = the correct color
    # board size = area of board
    # ---------------------------------------------
 
    if colorful:
        colors = COLORS_EXTENDED
    else:
        colors = COLORS
    l = []
    for _ in range(copy):
        l += [cell(color) for color in colors]
    # ------------------------------------------
    # for color in color_pool:
    #     print('loop start')
    #     diff = board_size - len(l)
    #     if diff >= num_players:
    #         print('case1')
    #         for _ in range(num_players):
    #             l+=[cell(color)]
    #     else:
    #         print('case2')
    #         for _ in range(diff):
    #             l+=[cell(color)]
    #     print(len(l))
    # ---------------------------------------
    rest = board_size - len(l)
    for i in range(rest):
        l.append(cell(colors[rd.randint(0,len(colors)-1)]))
    rd.shuffle(l)
    return l

# the main game board
class game_board:
    # board = board, size = length of each side
    def __init__(self, board, size=GRID_SIZE):
        self.board = board
        self.size = size

    def __str__(self) -> str:
        view = []
        for row in self.board:
            temp = []
            for obj in row:
                if obj.status == 0:
                    temp.append(obj.color)
                else:
                    temp.append(obj.status)
            view.append(temp)
        return draw(view)
    
    # set the status of a cell at row,col of the board to be = player_num
    def cell_status(self,player_num,row,col):
        self.board[row][col].status = player_num

    def player_place_marker(self,pN,row,col):
        self.cell_status(pN.num, row, col)
        pN.add_score()


# players
class player:
    # player number, player name, their score
    def __init__(self, num, name, score=0) -> None:
        self.num = num
        self.name = name
        self.score = score

    def add_score(self, n=1):
        self.score += n

# ---------------------------------------------------------------------------------------------------

def main():
    cb = color_board()
    cb_matrix = to_square_matrix(cb)
    main = game_board(cb_matrix)
    print(main)
    main.cell_status(2,3,3)
    print(main)

# main()
