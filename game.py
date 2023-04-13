import pygame
import bbc2
from sys import exit

# setup
GRID_SIZE = 5
COLORS = ['r','o','y','g','b','p']
INFOS = {'r': ['crimson', 'RED'], 'o': ['darkorange', 'ORANGE'], 'y': ['gold', 'YELLOW'], 'g': ['chartreuse3', 'GREEN'], 'b': ['steelblue2', 'BLUE'], 'p': ['mediumpurple', 'PURPLE']}
size = width, height = (800,800)

pygame.init()

screen = pygame.display.set_mode(size)
game_name = pygame.display.set_caption("The game board")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    k= str(input("Enter the key: "))
    screen.fill(INFOS[k][0])
    pygame.display.update()
    clock.tick(60)
