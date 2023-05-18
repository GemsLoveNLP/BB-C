import pygame
from sys import exit
import bbc2
import time
import random as rd

from pyvidplayer import Video


#todo config here -------------
DIFF = {'NORMAL':{'wait':1, 'max':2, 'max_wait':90},'HARD':{'wait':0.8, 'max':4, 'max_wait':60}}

SIZE = 660     
ROUND = 10      
FRAMERATE = 30
ANIMATION_THRESHOLD = 60
CIRCLE_THRESHOLD = 30
NUM_PLAYER = 4
GRID = 6
DIFFICULTY = 'NORMAL'
#todo -------------------------

# initializing

pygame.init()
screen = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption('Game Board')
clock = pygame.time.Clock()

p1 = bbc2.player(1,'Sirkle')
p2 = bbc2.player(2,'Sektor')
p3 = bbc2.player(3,'Parrod')
p4 = bbc2.player(4,'Hexate')
p_list = [p1, p2, p3, p4]
player_list = p_list[0:NUM_PLAYER]

# play a background color (useful when wanting to test screen)
def play_color(color,size=SIZE):
    bg = pygame.surface.Surface((size,size))
    bg.fill(color)
    screen.blit(bg,(0,0))

# get the ".png" file name followed by n length string number
def get_file_name(dir, i, folder_size, n=4):
    i = i%folder_size
    string = dir+"0"*(n-len(str(i)))+str(i)+".png"
    return string

# play a .png file
def play_vid(dir,size=SIZE, coord = (0,0)):
    img = pygame.image.load(dir)
    trans_img = pygame.transform.scale(img,(size,size))
    screen.blit(trans_img,coord)

# create a begin screen
# def begin_screen(i,size=SIZE):
    # background = pygame.surface.Surface((size,size))
    # background.fill('black')
    # screen.blit(background,(0,0))
    # header_font = pygame.font.Font(None,size//8)
    # header = header_font.render('Press any key to start', True, 'yellow')
    # header_rect = header.get_rect(center=(size//2,size//2))
    # screen.blit(header, header_rect)
    # img = pygame.image.load(f"tutorial\\tutorial ({i%531}).png")
    # trans_img = pygame.transform.scale(img,(size,size))
    # screen.blit(trans_img,(0,0))

# create a text screen and return the solution
def text_screen(size=SIZE, exclude=dict()):
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

# create sequences of text screens before creating a color screen with the correct colors
def game_screens(size=SIZE):
    # repetition = number of times the text screen would show
    global correct_color_list, correct_list
    difficulty = DIFF[DIFFICULTY]
    repetition = rd.randint(1,difficulty['max'])
    correct_color_list = []
    correct_list = []
    for i in range(repetition):
        correct_color = text_screen(size=size, exclude=correct_color_list)
        pygame.display.update()
        correct_color_list.append(correct_color['text_color'])
        correct_list.append(correct_color)
        time.sleep(difficulty['wait'])
    true_correct_color_list = list(set(correct_color_list))
    print(correct_list)
    return color_screen(true_correct_color_list,size=size)

# create a screen of dynamic scores rank from best to worst vertically
def score_screen(size=SIZE):
    background = pygame.surface.Surface((size,size))
    background.fill('white')
    screen.blit(background,(0,0))
    header_font = pygame.font.Font(None,size//8)
    header = header_font.render('SCORE', True, 'red4')
    header_rect = header.get_rect(center=(size//2,size//9))
    screen.blit(header, header_rect)
    body_font = pygame.font.Font(None,size//15)
    d = dict()
    for p in player_in_game:
        d[p.name] = p.score
    p_dict = sorted(d,key=d.get)[::-1]
    i = 0  
    for p in p_dict:
        body_text = f'{p}: {d[p]//60}'      #! this is just a quick fix
        body = body_font.render(body_text, True, bbc2.RANK_COLORS[i])
        body_rect = body.get_rect(center=(size//2,size//3.5+i*size//8))
        screen.blit(body, body_rect)
        i+=1
    inst = header_font.render('Press any key to start',True, 'darkorange')
    inst_rect = inst.get_rect(center=(size//2,size - size//6))
    screen.blit(inst, inst_rect)

# create the circle that will flash black and white
def animate_circle(name, wait, time, size=SIZE):
    true_x = size//2
    true_y = size//2
    img = pygame.image.load(name)
    freq = time*15
    real_size = size//freq*wait
    fx = pygame.transform.scale(img, (real_size, real_size))
    fx_rect = fx.get_rect(center=(true_x,true_y))
    screen.blit(fx,fx_rect)

# animate the correct piece placement
def animate_winner(xyplayer_list, video_status, size=SIZE):
    # x, y is coordinate of grid slot 
    for xy in xyplayer_list:
        x = xy[0]
        y = xy[1]
        true_x = x*size//GRID
        true_y = y*size//GRID
        if xy[2] == 1:
            directory_anime = "กลมวืาง\\circle (1)"
            name_anime = get_file_name(directory_anime, video_status, 112, n=3)
        elif xy[2] == 2:
            directory_anime = "พายวิ้ง\\พายวิ้ง (1)"
            name_anime = get_file_name(directory_anime, video_status, 96, n=3)
        elif xy[2] == 3:
            directory_anime = "ใบ\\bi"
            name_anime = get_file_name(directory_anime, video_status, 112, n=3)
        elif xy[2] == 4:
            directory_anime = "เหลี่ยม\\hexa"
            name_anime = get_file_name(directory_anime, video_status, 112, n=3)
        play_vid(name_anime,size=SIZE//6,coord=(true_x,true_y))

# draw a static board from the recorded main
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

# psuedo code functions----------------------------------------------------------------------

# take photo to be analyze
def take_photo():
    return 0

# get the player.number of the winning player at the slot x,y if none wins then return False
def get_winner(x,y):
    if (x,y) == (0,0):return 0
    return 1

# get the piece color of the slot x,y if none then return 'black
def get_color(x,y):
    return 1

def get_cornor_winner():
    return sum([0 if get_color(x,y) != '0' else 1 for x,y in [(0,0,),(0,5),(5,5),(5,0)]]) == 0

# Note: pls switch the functions below in the main loop after finish (line 408)

#! for demo only, the real one is below
def find_correct_grid():
    xy_list = []
    for correct_color in correct_color_list:
        escape = False
        for y in range(GRID):
            for x in range(GRID):
                winner = get_winner(x,y)
                if main_board.board[y][x].color == correct_color and winner != 0:
                    # print(x,y)
                    xy_list.append((x,y,winner))
                    player_list[winner-1].add_score(1)
                    escape = True
                if escape:break
            if escape:break
    return xy_list

# find the grid that the animations will be playing on return (x,y, winning_player.number)
def find_correct():
    xy_list = []
    for correct_color in correct_list:
        for y in range(GRID):
            for x in range(GRID):
                if main_board.board[y][x].color == correct_color['text_color'] and get_color(x,y) == correct_list['text']:
                    # print(x,y)
                    win_player_number = get_winner(x,y)
                    player_list[win_player_number-1].add_score(1)
                    xy_list.append((x,y,win_player_number))
    return xy_list

# ------------------------------------------------------------------------------------------------------------

# ? status represents the game status
# ? status list: 
# ?    - begin = load screen
# ?    - join = start page to do num player settings
# ?    - mode_select = screen to do difficulty settings
# ?    - tutorial = video of the tutorial
# ?    - game = display the text then the board
# ?    - hold = hold the game board in place for checking
# ?    - animate_white = animation of white circle to take sillouhette picture
# ?    - animate_black = animation of black circle to take colored picture
# ?    - animate = animation of placement
# ?    - score = show score board and press to continue

# ---------------------------------------------------------

def main_game():
    global main_board, player_in_game, DIFFICULTY

    status = 'begin'
    
    video_status = 0
    animation_count = 0
    wait = 0
    join_key = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    circle_animation_status = False
                    p1.set_status(True)
                    join_key = True
                if event.key == pygame.K_2:
                    sector_animation_status = False
                    p2.set_status(True)
                    join_key = True
                if event.key == pygame.K_3:
                    pill_animation_status = False
                    p3.set_status(True)
                    join_key = True
                if event.key == pygame.K_4:
                    hex_animation_status = False
                    p4.set_status(True)
                    join_key = True

                if event.key == pygame.K_1:
                    beginner_animation_status = False
                    DIFFICULTY = 'NORMAL'
                if event.key == pygame.K_2:
                    expert_animation_status = False
                    DIFFICULTY = 'HARD'

                if status == 'begin':
                    circle_animation_status = True
                    sector_animation_status = True
                    pill_animation_status = True
                    hex_animation_status = True
                    status = 'join'
                    video_status = 0
                elif status == 'join' and event.key == pygame.K_SPACE:
                    beginner_animation_status = True
                    expert_animation_status = True
                    player_in_game = []
                    for pi in [p1,p2,p3,p4]:
                        if pi.status:
                            player_in_game.append(pi)
                    print(player_in_game)
                    status = 'mode_select'
                    video_status = 0
                elif status == 'mode_select':
                    print(DIFFICULTY)
                    status = 'tutorial'
                    video_status = 0
                elif status == 'tutorial':
                    status = 'game'
                elif status == 'score':
                    status = 'game'

        # print(animation_status)

        if status == 'begin':
            directory = "1-loading\\loding screen (2)"
            name = get_file_name(directory, video_status, 908)
            play_vid(name,size=SIZE)
            video_status+=1
        elif status == 'join':
            directory = f"2-join the game\\join"
            name = get_file_name(directory, video_status, 1910)
            play_vid(name,size=SIZE)
            if circle_animation_status:
                directory_anime = "กลมวืาง\\circle (1)"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(0,0))
            if hex_animation_status:
                directory_anime = "เหลี่ยม\\hexa"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(0,SIZE/6*5))
            if sector_animation_status:
                directory_anime = "พายวิ้ง\\พายวิ้ง (1)"
                name_anime = get_file_name(directory_anime, video_status, 96, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(SIZE/6*5,0))
            if pill_animation_status:
                directory_anime = "ใบ\\bi"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(SIZE/6*5,SIZE/6*5))
            video_status+=1
        elif status == 'mode_select':
            directory = "3-select mode\\select"
            name = get_file_name(directory, video_status, 1302)
            play_vid(name,size=SIZE)
            if beginner_animation_status:
                directory_anime = "กลมวืาง\\circle (1)"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(0,SIZE/6*5))
            if expert_animation_status:
                directory_anime = "กลมวืาง\\circle (1)"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(SIZE/6*5,SIZE/6*5))
            video_status+=1
        elif status == 'tutorial':
            directory = "4-starting\\starting"
            name = get_file_name(directory, video_status, 414)
            play_vid(name,size=SIZE)
            video_status+=1
        elif status == 'game':
            cb_mat = game_screens(size=SIZE)
            main_board = bbc2.game_board(cb_mat)
            print(main_board)
            status = 'hold'
            wait = 0
        elif status == 'hold' and wait > DIFF[DIFFICULTY]['max_wait']:
            status = 'animate_white'
            wait = 0
        elif status == 'animate_white':
            if wait > CIRCLE_THRESHOLD:
                take_photo()    #! psuedo function
                status = 'animate_black'
                wait = 0
            else:
                # print('black')
                animate_circle('black_cir.png', wait, 1, size=SIZE)
        elif status == 'animate_black':
            if wait > CIRCLE_THRESHOLD:
                take_photo()    #! psuedo function
                status = 'animate'
                wait = 0
            else:
                # print('white')
                animate_circle('white_cir.png', wait, 1, size=SIZE)
        elif status == 'animate':
            static_board_screen(size=SIZE)
            animate_winner(find_correct_grid(),animation_count,size=SIZE) #!find_correct_grid() has to be changed to find_correct
            animation_count+=1
        elif status == 'score':
            score_screen(size=SIZE)


        if animation_count >= ANIMATION_THRESHOLD:
            status = 'score'
            animation_count = 0

        wait+=1

        pygame.display.update()
        # time.sleep(bbc2.NORMAL['wait'])
        clock.tick(FRAMERATE)

# full_game('Gems.mp4', 'Gems.mp4', size=SIZE)

# def test_func(f):
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()

#         f('white')
#         pygame.display.update()
#         # time.sleep(bbc2.NORMAL['wait'])
#         clock.tick(FRAMERATE)

# test_func(play_color)

def main_game2():
    global main_board, player_in_game, DIFFICULTY

    status = 'begin'
    
    video_status = 0
    animation_count = 0
    wait = 0

    join_key = False
    mode_key = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1 or get_winner(0,0) != 0:
                    circle_animation_status = False
                    p1.set_status(True)
                    join_key = True
                if event.key == pygame.K_2 or get_winner(5,0) != 0:
                    sector_animation_status = False
                    p2.set_status(True)
                    join_key = True
                if event.key == pygame.K_3 or get_winner(5,5) != 0:
                    pill_animation_status = False
                    p3.set_status(True)
                    join_key = True
                if event.key == pygame.K_4 or get_winner(0,5) != 0:
                    hex_animation_status = False
                    p4.set_status(True)
                    join_key = True

                if event.key == pygame.K_1 or get_winner(0,5) != 0:
                    print('1')
                    beginner_animation_status = False
                    DIFFICULTY = 'NORMAL'
                    mode_key = True
                if event.key == pygame.K_2 or get_winner(5,5) != 0:
                    print('2')
                    expert_animation_status = False
                    DIFFICULTY = 'HARD'
                    mode_key = True

                if status == 'begin':
                    circle_animation_status = True
                    sector_animation_status = True
                    pill_animation_status = True
                    hex_animation_status = True
                    status = 'join'
                    video_status = 0
                elif status == 'join' and (event.key == pygame.K_SPACE  or (get_cornor_winner() and join_key)):
                    beginner_animation_status = True
                    expert_animation_status = True
                    player_in_game = []
                    for pi in [p1,p2,p3,p4]:
                        if pi.status:
                            player_in_game.append(pi)
                    print(player_in_game)
                    status = 'mode_select'
                    video_status = 0
                elif status == 'mode_select' and mode_key:
                    print(DIFFICULTY)
                    status = 'tutorial'
                    video_status = 0
                elif status == 'tutorial':
                    status = 'game'
                elif status == 'score':
                    status = 'game'

        # print(animation_status)

        if status == 'begin':
            directory = "1-loading\\loding screen (2)"
            name = get_file_name(directory, video_status, 908)
            play_vid(name,size=SIZE)
            video_status+=1
        elif status == 'join':
            directory = f"2-join the game\\join"
            name = get_file_name(directory, video_status, 1910)
            play_vid(name,size=SIZE)
            if circle_animation_status:
                directory_anime = "กลมวืาง\\circle (1)"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(0,0))
            if hex_animation_status:
                directory_anime = "เหลี่ยม\\hexa"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(0,SIZE/6*5))
            if sector_animation_status:
                directory_anime = "พายวิ้ง\\พายวิ้ง (1)"
                name_anime = get_file_name(directory_anime, video_status, 96, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(SIZE/6*5,0))
            if pill_animation_status:
                directory_anime = "ใบ\\bi"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(SIZE/6*5,SIZE/6*5))
            video_status+=1

            take_photo()

            if get_winner(0,0) != 0:
                    circle_animation_status = False
                    p1.set_status(True)
                    join_key = True
            if get_winner(5,0) != 0:
                    sector_animation_status = False
                    p2.set_status(True)
                    join_key = True
            if get_winner(5,5) != 0:
                    pill_animation_status = False
                    p3.set_status(True)
                    join_key = True
            if get_winner(0,5) != 0:
                    hex_animation_status = False
                    p4.set_status(True)
                    join_key = True      

        elif status == 'mode_select':
            directory = "3-select mode\\select"
            name = get_file_name(directory, video_status, 1302)
            play_vid(name,size=SIZE)
            if beginner_animation_status:
                directory_anime = "กลมวืาง\\circle (1)"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(0,SIZE/6*5))
            if expert_animation_status:
                directory_anime = "กลมวืาง\\circle (1)"
                name_anime = get_file_name(directory_anime, video_status, 112, n=3)
                play_vid(name_anime,size=SIZE//6,coord=(SIZE/6*5,SIZE/6*5))
            video_status+=1
        elif status == 'tutorial':
            directory = "4-starting\\starting"
            name = get_file_name(directory, video_status, 414)
            play_vid(name,size=SIZE)
            video_status+=1
        elif status == 'game':
            cb_mat = game_screens(size=SIZE)
            main_board = bbc2.game_board(cb_mat)
            print(main_board)
            status = 'hold'
            wait = 0
        elif status == 'hold' and wait > DIFF[DIFFICULTY]['max_wait']:
            status = 'animate_white'
            wait = 0
        elif status == 'animate_white':
            if wait > CIRCLE_THRESHOLD:
                take_photo()    #! psuedo function
                status = 'animate_black'
                wait = 0
            else:
                # print('black')
                animate_circle('black_cir.png', wait, 1, size=SIZE)
        elif status == 'animate_black':
            if wait > CIRCLE_THRESHOLD:
                take_photo()    #! psuedo function
                status = 'animate'
                wait = 0
            else:
                # print('white')
                animate_circle('white_cir.png', wait, 1, size=SIZE)
        elif status == 'animate':
            static_board_screen(size=SIZE)
            animate_winner(find_correct_grid(),animation_count,size=SIZE) #!find_correct_grid() has to be changed to find_correct
            animation_count+=1
        elif status == 'score':
            score_screen(size=SIZE)


        if animation_count >= ANIMATION_THRESHOLD:
            status = 'score'
            animation_count = 0

        wait+=1

        pygame.display.update()
        # time.sleep(bbc2.NORMAL['wait'])
        clock.tick(FRAMERATE)

main_game()