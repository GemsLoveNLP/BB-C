import pygame
from sys import exit
import bbc2
import time
import random as rd


# config here-----
SIZE = 700      
ROUND = 10      
FRAMERATE = 30  
# ----------------

pygame.init()
screen = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption('Game Board')
clock = pygame.time.Clock()

p1 = bbc2.player(1,'Ren',1)
p2 = bbc2.player(2,'Qii',0)
p3 = bbc2.player(3,'Nul',5)
p4 = bbc2.player(4,'Dsir',7)
player_list = [p1, p2, p3, p4]

# cb_matrix = bbc2.to_square_matrix(bbc2.color_board('b'))
# main = bbc2.game_board(cb_matrix)
# print(main)
# main.player_place_marker(p1,1,1)
# main.player_place_marker(p2,2,1)
# main.player_place_marker(p3,1,3)
# main.player_place_marker(p4,1,4)
# print(main)

def begin_screen(size=700):
    background = pygame.surface.Surface((size,size))
    background.fill('black')
    screen.blit(background,(0,0))
    header_font = pygame.font.Font(None,size//8)
    header = header_font.render('Press any key to start', True, 'yellow')
    header_rect = header.get_rect(center=(size//2,size//2))
    screen.blit(header, header_rect)

def text_screen(size=700):
    test_font = pygame.font.Font(None,size//8)
    d = bbc2.text_screen_random(colorful=True)
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

def color_screen(correct_color, size=700):
    cb_matrix = bbc2.to_square_matrix(bbc2.color_board(correct_color,colorful=True))
    for y in range(5):
        for x in range(5):
            color_pixel = pygame.surface.Surface((size//5,size//5))
            color_pixel.fill(bbc2.INFOS[cb_matrix[y][x].color][0])
            screen.blit(color_pixel,(size//5*x,size//5*y))
    bar_surface = pygame.image.load('5x5 Grid.png')
    trans_bar = pygame.transform.scale(bar_surface,(size,size))
    screen.blit(trans_bar,(0,0))
    return cb_matrix

def game_screens(repetition=0, size=700, difficulty=bbc2.NORMAL):
    if repetition < 1:
        repetition = rd.randint(1,difficulty['max'])
    correct_color_list = []
    for i in range(repetition):
        correct_color = text_screen(size=size)
        pygame.display.update()
        correct_color_list.append(correct_color['text_color'])
        time.sleep(difficulty['wait'])
    true_correct_color_list = list(set(correct_color_list))
    color_screen(true_correct_color_list,size=size)


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


# ------------------------------------------------------------------------------------------------------------

# status represents the game status
# status list: 
#     - begin = start page to use settings
#     - game = display teh text then the board
#     - hold = hold the game board in place for checking
#     - animate = animation of placement
#     - score = show score board and press to continue

# ---------------------------------------------------------

status = 'begin'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # print(status)

    # color_screen(bbc2.rand_color())

    # text_screen()

    game_screens()

    pygame.display.update()
    time.sleep(bbc2.NORMAL['wait'])
    clock.tick(FRAMERATE)

