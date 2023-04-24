import pygame
import cv2

video = cv2.VideoCapture("tutorial.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)

window = pygame.display.set_mode((700,700))
clock = pygame.time.Clock()

run = success
i = 0
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # success, video_image = video.read()
    # if success:
    #     video_surf = pygame.image.frombuffer(
    #         video_image.tobytes(), video_image.shape[1::-1], "BGR")
    # else:
    #     run = False
    # window.blit(video_surf, (0, 0))
    # pygame.display.flip()
    
    img = pygame.image.load(f"C:\\Users\\user\\Desktop\\Python\\BBC\\tutorial\\tutorial ({i%531}).png")
    # img = pygame.image.load("ring.png")
    timg = pygame.transform.scale(img,(700,700))
    window.blit(timg, (0,0))
    pygame.display.update()

    i+=1

pygame.quit()
exit()