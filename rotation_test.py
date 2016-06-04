import sys
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

pygame.init()
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Spinning Planet")
clock = pygame.time.Clock()
image = pygame.image.load("Images/Creatures/glacialPuffer.png").convert()
img_rect = image.get_rect()
img_rect.x = 100
img_rect.y = 200
angle = 0
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
    angle += 1
    if angle >= 360:
        angle = 0
    rot_image = pygame.transform.rotate(image, angle)
    rot_im_rect = rot_image.get_rect()
    rot_im_rect.center = img_rect.center
    screen.blit(rot_image, rot_im_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
