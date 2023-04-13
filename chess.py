import pygame

pygame.init()

size = width, height = (800,800)

# width = height = int(input('Let\'s draw a chessboard =) \nSpecify the window size from 100 to 1500 pixels (it will be in 1: 1 format): \n')) 
# size = (width, height)
screen = pygame.display.set_mode(size)

rows = cols = 5 #int(input('Specify the desired number of squares, I will raise them to the square and build a chessboard: \n'))
square_size = width / rows


game_name = pygame.display.set_caption("The chess board")

# rgb
white_color = (255, 230, 153)
black_color = (128, 64, 0)

def draw_squares(screen):
    screen.fill(white_color)
    # for row in range(rows):
    #     for col in range(row % 2, rows, 2):
    #         pygame.draw.rect(screen, black_color, (col * square_size, row*square_size, square_size, square_size))

while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()
    # draw_squares(screen)
    screen.fill(white_color)
    pygame.display.update()

pygame.quit()