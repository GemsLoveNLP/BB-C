import pygame
from sys import exit
import bbc2
import time
import random as rd

from pyvidplayer import Video


#todo config here -------------
DIFF = {'NORMAL':{'wait':1, 'max':2},'HARD':{'wait':0.8, 'max':5}}

SIZE = 750      
ROUND = 10      
FRAMERATE = 30
ANIMATION_THRESHOLD = 20
NUM_PLAYER = 4
GRID = 6
DIFFICULTY = 'HARD'
#todo -------------------------

pygame.init()
screen = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption('Game Board')
clock = pygame.time.Clock()

p1 = bbc2.player(1,'Sirkle')
p2 = bbc2.player(2,'Sektor')
p3 = bbc2.player(3,'Soapoo')
p4 = bbc2.player(4,'BeeHex')
p_list = [p1, p2, p3, p4]
player_list = p_list[0:NUM_PLAYER]


# cb_matrix = bbc2.to_square_matrix(bbc2.color_board('b'))
# main = bbc2.game_board(cb_matrix)
# print(main)
# main.player_place_marker(p1,1,1)
# main.player_place_marker(p2,2,1)
# main.player_place_marker(p3,1,3)
# main.player_place_marker(p4,1,4)
# print(main)

# get the file name
def get_file_name(dir, i, folder_size):
    i = i%folder_size
    string = dir+"0"*(4-len(str(i)))+str(i)+".png"
    return string

# play a folder frame by frame
def play_vid(dir,size=700, coord = (0,0)):
    img = pygame.image.load(dir)
    trans_img = pygame.transform.scale(img,(size,size))
    screen.blit(trans_img,coord)

# create a begin screen
def begin_screen(i,size=700):
    # background = pygame.surface.Surface((size,size))
    # background.fill('black')
    # screen.blit(background,(0,0))
    # header_font = pygame.font.Font(None,size//8)
    # header = header_font.render('Press any key to start', True, 'yellow')
    # header_rect = header.get_rect(center=(size//2,size//2))
    # screen.blit(header, header_rect)
    img = pygame.image.load(f"C:\\Users\\user\\Desktop\\Python\\BBC\\tutorial\\tutorial ({i%531}).png")
    trans_img = pygame.transform.scale(img,(size,size))
    screen.blit(trans_img,(0,0))

# create a text screen and return the solution
def text_screen(size=700, exclude=[]):
    test_font = pygame.font.Font(None,size//8)
    d = bbc2.text_screen_random(colorful=True, color_to_not_include=exclude)
    background_surface = pygame.Surface((size,size))
    background_surface.fill(bbc2.INFOS[d['background']][0])
    screen.blit(background_surface,(0,0))
    text_surface1 = test_font.render(bbc2.INFOS[d['text']][1].upper(), True ,bbc2.INFOS[d['text_color']][0])
    text_surface2 = pygame.transform.rotate(text_surface1,90)
    text_surface3 = pygame.transform.rotate(text_surface1,180)
    text_surface4 = pygame.transform.rotate(text_surface1,270)
    text_rect_1 = text_surface1.get_rect(center=(size//2,size-size//10))
    text_rect_2 = text_surface2.get_rect(center=(size-size//10,size//2))
    text_rect_3 = text_surface3.get_rect(center=(size//2,size//10))
    text_rect_4 = text_surface4.get_rect(center=(size//10,size//2))
    screen.blit(text_surface1,text_rect_1)
    screen.blit(text_surface2,text_rect_2)
    screen.blit(text_surface3,text_rect_3)
    screen.blit(text_surface4,text_rect_4)
    return d

# def color_screen_old(size=700):
#     for y in range(5):
#         for x in range(5):
#             color_pixel = pygame.surface.Surface((size//5,size//5))
#             color_pixel.fill(bbc2.INFOS[main.board[y][x].color][0])
#             screen.blit(color_pixel,(size//5*x,size//5*y))
#             if main.board[y][x].status != 0:
#                 icon_surface = pygame.image.load(f'{main.board[y][x].status}.png')
#                 trans_icon = pygame.transform.scale(icon_surface,(size//5,size//5))
#                 screen.blit(trans_icon,(size//5*x,size//5*y))
#     bar_surface = pygame.image.load('5x5 Grid.png')
#     trans_bar = pygame.transform.scale(bar_surface,(size,size))
#     screen.blit(trans_bar,(0,0))

# create a color screen and return the associated GRIDxGRID list of cell objects 
def color_screen(correct_color, size=SIZE):
    # correct_color is a list that contains the correct color initials
    cb_matrix = bbc2.to_square_matrix(bbc2.color_board(correct_color,colorful=True,num_players=NUM_PLAYER))
    for y in range(GRID):
        for x in range(GRID):
            color_pixel = pygame.surface.Surface((size//GRID,size//GRID))
            color_pixel.fill(bbc2.INFOS[cb_matrix[y][x].color][0])
            screen.blit(color_pixel,(size//GRID*x,size//GRID*y))
    bar_surface = pygame.image.load('6x6.png')
    trans_bar = pygame.transform.scale(bar_surface,(size,size))
    screen.blit(trans_bar,(0,0))
    return cb_matrix

# create 1-4 text screen before creating a color screen with the correct colors
def game_screens(size=700):
    # repetition = number of times the text screen would show
    global correct_color_list
    difficulty = DIFF[DIFFICULTY]
    repetition = rd.randint(1,difficulty['max'])
    correct_color_list = []
    for i in range(repetition):
        correct_color = text_screen(size=size, exclude=correct_color_list)
        pygame.display.update()
        correct_color_list.append(correct_color['text_color'])
        time.sleep(difficulty['wait'])
    true_correct_color_list = list(set(correct_color_list))
    return color_screen(true_correct_color_list,size=size)

# create a screen of dynamic scores rank from best to worst vertically
def score_screen(size=700):
    background = pygame.surface.Surface((size,size))
    background.fill('black')
    screen.blit(background,(0,0))
    header_font = pygame.font.Font(None,size//8)
    header = header_font.render('SCORE', True, 'yellow')
    header_rect = header.get_rect(center=(size//2,size//9))
    screen.blit(header, header_rect)
    body_font = pygame.font.Font(None,size//12)
    d = dict()
    for p in player_list:
        d[p.name] = p.score
    p_dict = sorted(d,key=d.get)[::-1]
    i = 0  
    for p in p_dict:
        body_text = f'{p}: {d[p]}'
        body = body_font.render(body_text, True, bbc2.RANK_COLORS[i])
        body_rect = body.get_rect(center=(size//2,size//3.5+i*size//8))
        screen.blit(body, body_rect)
        i+=1
    inst = header_font.render('Press any key to start',True, 'lawngreen')
    inst_rect = inst.get_rect(center=(size//2,size - size//6))
    screen.blit(inst, inst_rect)

# animate a png to get progressively larger
def animate_circle(xy_list, scale, size=700):
    # x, y is coordinate of grid slot 
    coor_list = []
    for xy in xy_list:
        x = xy[0]
        y = xy[1]
        coor_x = x*size//GRID + size//(GRID*2)
        coor_y = y*size//GRID + size//(GRID*2)
        coor_list.append((coor_x,coor_y))
    for xy in coor_list:
        true_x = xy[0]
        true_y = xy[1]
        img = pygame.image.load('ring.png')
        real_size = size//80+size//120*scale
        fx = pygame.transform.scale(img, (real_size, real_size))
        fx_rect = fx.get_rect(center=(true_x,true_y))
        screen.blit(fx,fx_rect)

# draw a board from main
def static_board_screen(size=SIZE):
    for y in range(GRID):
        for x in range(GRID):
            color_pixel = pygame.surface.Surface((size//GRID,size//GRID))
            color_pixel.fill(bbc2.INFOS[main_board.board[y][x].color][0])
            screen.blit(color_pixel,(size//GRID*x,size//GRID*y))
            if main_board.board[y][x].status != 0:
                icon_surface = pygame.image.load(f'{main.board[y][x].status}.png')
                trans_icon = pygame.transform.scale(icon_surface,(size//GRID,size//GRID))
                screen.blit(trans_icon,(size//GRID*x,size//GRID*y))
    bar_surface = pygame.image.load('6x6.png')
    trans_bar = pygame.transform.scale(bar_surface,(size,size))
    screen.blit(trans_bar,(0,0))

# -----------------------------------------------------------------------------------------------------------

# psuedo code functions

def get_winner():
    player_number = rd.randint(1,NUM_PLAYER)
    return player_number

def find_correct_grid():
    xy_list = []
    for correct_color in correct_color_list:
        escape = False
        for y in range(GRID):
            for x in range(GRID):
                if main_board.board[y][x].color == correct_color:
                    # print(x,y)
                    xy_list.append((x,y))
                    escape = True
                if escape:break
            if escape:break
    return xy_list

# ------------------------------------------------------------------------------------------------------------

# ? status represents the game status
# ? status list: 
# ?    - begin = start page to use settings
# ?    - game = display the text then the board
# ?    - hold = hold the game board in place for checking
# ?    - animate = animation of placement
# ?    - score = show score board and press to continue

# ---------------------------------------------------------

def main_game():
    global main_board
    
    video_status = 0

    status = 'begin'
    animation_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if status == 'begin' and event.type == pygame.KEYDOWN:
                print("event0")
                status = 'select_player'
                video_status = 0
            elif status == 'select_player' and event.type == pygame.KEYDOWN:
                print("event0.5")
                status = 'game'
            elif status == 'hold' and event.type == pygame.KEYDOWN:
                print("event1")
                #!----------------------------------------------
                for _ in range(len(correct_color_list)):
                    player_list[get_winner()-1].score+=1
                #!----------------------------------------------
                animation_count = 0
                status = 'animate'
            elif status == 'score' and event.type == pygame.KEYDOWN:
                print("event2")
                status = 'game'

        # print(status)

        if status == 'begin':
            directory = "C:\\Users\\user\\Desktop\\Python\\BBC\\intro + player_selection\\start to place to join the game"
            name = get_file_name(directory, video_status, 3354)
            directory_anime = "C:\\Users\\user\\Desktop\\Python\\BBC\\effect_circle\\effect_circle"
            name_anime = get_file_name(directory_anime, video_status, 118)
            play_vid(name,size=SIZE)
            play_vid(name_anime,size=SIZE//6,coord=(0,0))
            video_status+=1
        elif status == 'select_player':
            name = f"C:\\Users\\user\\Desktop\\Python\\BBC\\player_select\\player_number ({video_status%2683+1}).png"
            play_vid(name,size=SIZE)
            video_status+=1
        elif status == 'score':
            score_screen(size=SIZE)
        elif status == 'game':
            cb_mat = game_screens(size=SIZE)
            main_board = bbc2.game_board(cb_mat)
            print(main_board)
            status = 'hold'
        elif status == 'animate':
            static_board_screen(size=SIZE)
            animate_circle(find_correct_grid(),animation_count,size=SIZE) #!find_correct_grid()
            animation_count+=1

        if animation_count >= ANIMATION_THRESHOLD:
            status = 'score'
            animation_count = 0

        pygame.display.update()
        # time.sleep(bbc2.NORMAL['wait'])
        clock.tick(FRAMERATE)


# def full_game(name, name2, size=700):
#     global NUM_PLAYER, DIFFICULTY

#     # first video

#     vid = Video(name)
#     vid.set_size((size,size))

#     # similar to status, but is used to select the correct video to show

#     vid_status = 0

#     # vid.draw(screen, (0,0))
#     # pygame.display.update()

#     while True:
#         vid.draw(screen, (0,0))
#         # sprite = pygame.image.load('1.png')
#         # screen.blit(sprite,(0,0))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             if event.type == pygame.KEYDOWN and vid_status == 0:
                
#                 #todo set the number of players using the camera
#                 NUM_PLAYER = 4

#                 vid.close()

#                 pygame.display.update()

#                 vid_status+=1
#                 vid = Video(name2)
#                 vid.set_size((size,size))
#                 vid.draw(screen, (0,0))

#             elif event.type == pygame.KEYDOWN and vid_status == 1:
                
#                 #todo set the difficulty using the camera
#                 DIFFICULTY = 'NORMAL'

#                 vid.close()

#                 pygame.display.update()

#                 main_game()


main_game()

# full_game('Gems.mp4', 'Gems.mp4', size=SIZE)