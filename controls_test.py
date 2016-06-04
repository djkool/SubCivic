
import pygame

pygame.init()

screenW = 1280
screenH = 720
FPS = 60
play = True


def set_pos(actor, x, y):
    actor.rect.x = x
    actor.rect.y = y

pygame.display.set_caption('SubCivic')
screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()

screen.fill((0, 239, 192))

depth = 0
speed = 0
direction = 0

thrust = 0
turn = 0
buoyancy = 0

font = pygame.font.Font(None, 25)
bar = pygame.Surface((10, 200))
bar.fill((75, 75, 85))


class Control(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40, 16))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

bControl = Control()
movebtn = False

while play:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            play = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mypos = pygame.mouse.get_pos()
            if 400 + buoyancy < mypos[1] < 416 + buoyancy and 400 < mypos[0] < 440:
                movebtn = True
        elif event.type == pygame.MOUSEMOTION:
            if movebtn:
                mypos = pygame.mouse.get_pos()
                if mypos[1] > 500:
                    buoyancy = 100
                elif mypos[1] < 300:
                    buoyancy = -100
                else:
                    buoyancy = mypos[1] - 400
        elif event.type == pygame.MOUSEBUTTONUP:
            if movebtn:
                movebtn = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        thrust += .001
    elif keys[pygame.K_a]:
        thrust -= .001
    if keys[pygame.K_c]:
        turn += .001
    elif keys[pygame.K_z]:
        turn -= .001
    if keys[pygame.K_e] and buoyancy < 100:
        buoyancy += 1
    elif keys[pygame.K_q] and buoyancy > -100:
        buoyancy -= 1

    if not (depth < 0 > buoyancy):
        depth += buoyancy/10000

    screen.fill((0, 239, 192))
    text = font.render("Depth: " + str(round(depth)) + ' M', True, (0, 0, 0))
    screen.blit(text, (100, 100))
    text = font.render("Speed: " + str(round(speed)), True, (0, 0, 0))
    screen.blit(text, (100, 150))
    text = font.render(("Direction: " + str(round(direction)) + '\xb0' ), True, (0, 0, 0))
    screen.blit(text, (100, 200))
    screen.blit(bar, (415, 308))
    screen.blit(bControl.image, (400, 400 + buoyancy))

    pygame.display.update()

pygame.quit()
quit()
