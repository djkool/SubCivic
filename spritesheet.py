import pygame
import math

clock = pygame.time.Clock()

SCREEN_X=400
SCREEN_Y=400
#Screen size

SPRT_RECT_X=0
SPRT_RECT_Y=0
#This is where the sprite is found on the sheet

LEN_SPRT_X=20
LEN_SPRT_Y=22
#This is the length of the sprite
drawFPS = 0


screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Create the screen
sheet = pygame.image.load('Images/Creatures/glacialPuffer.png') #Load the sheet

sheet.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)) #Locate the sprite you want
draw_me = sheet.subsurface(sheet.get_clip()) #Extract the sprite you want

backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it

running = True

while running:
    clock.tick(10)
    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if SPRT_RECT_X == 100:
        SPRT_RECT_X = 0
    else:
        SPRT_RECT_X += 20

    sheet.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y))  # Locate the sprite you want
    draw_me = sheet.subsurface(sheet.get_clip())  # Extract the sprite you want
    draw_me = pygame.transform.scale(draw_me, (40, 44))

    pygame.display.update()
    screen.fill((0, 0, 0))
    for i in range(1):
        screen.blit(draw_me, backdrop)  # 'Blit' on the backdrop
    # Draw the sprite on the screen
    pygame.display.set_caption(str(math.ceil(clock.get_fps())))


pygame.quit()



