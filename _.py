import pygame
from sys import exit
import bbc2
import time


# config here-----
SIZE = 800      #|
# ----------------

pygame.init()
screen = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption('Game Board')
clock = pygame.time.Clock()

test_surface = pygame.Surface((700,700))
test_surface.fill('royalblue4')

cb_matrix = bbc2.to_square_matrix(bbc2.color_board())
main = bbc2.game_board(cb_matrix)
print(main)

def text_screen(size=700):
    test_font = pygame.font.Font(None,SIZE//8)
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

def color_screen(size=700):
    for y in range(5):
        for x in range(5):
            color_pixel = pygame.surface.Surface((size//5,size//5))
            color_pixel.fill(bbc2.INFOS[main.board[y][x].color][0])
            screen.blit(color_pixel,(size//5*x,size//5*y))
    bar_surface = pygame.image.load('bar.png')
    trans_bar = pygame.transform.scale(bar_surface,(size,size))
    screen.blit(trans_bar,(0,0))

def color_screen_example(size=700):
    cb_matrix = bbc2.to_square_matrix(bbc2.color_board(colorful=True))
    for y in range(5):
        for x in range(5):
            color_pixel = pygame.surface.Surface((size//5,size//5))
            color_pixel.fill(bbc2.INFOS[cb_matrix[y][x].color][0])
            screen.blit(color_pixel,(size//5*x,size//5*y))
    bar_surface = pygame.image.load('bar.png')
    trans_bar = pygame.transform.scale(bar_surface,(size,size))
    screen.blit(trans_bar,(0,0))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # screen.blit(test_surface,(0,0)) #(x,y)

    # text_screen(size=SIZE)

    color_screen_example(size=SIZE)
    
    pygame.display.update()
    
    time.sleep(1)
    clock.tick(30)

