"""
SubCivic, a submarine simulation, mining, and exploration game. Created by Wesley Barlow & Daniel Reis, 2016.
Writen in Python 3.5 and Pygame 1.9, feel free to learn, mod, or contribute. Party on.

Convert to .EXE file on Mac using PyInstaller
Run the following commands in Terminal
python3.5 -m pip install pyinstaller
open /Users/Wesxdz/PycharmProjects/SubCivic
pyinstaller starup.py
"""

from math import atan2, degrees
import pygame

pygame.init()


# Define import global variables and start display ---------------------------------------------------------------------

screenW = 1280  # Default resolution of FTL and Shiprekt, some users may not have high enough display res though
screenH = 720
FPS = 60  # Limit to 30?
zoom = 2

clock = pygame.time.Clock()
running = True
pause = False
mute = False

pygame.display.set_caption('SubCivic')  # Set window title (Doesn't work for Mac icon hover?)
pygame.display.set_icon(pygame.image.load('Images/UI/compass.png'))  # Game icon, 32x32
screen = pygame.display.set_mode((screenW, screenH), pygame.HWSURFACE)
# ,pygame.FULLSCREEN (To start in fullscreen)

background = pygame.Surface((screenW, screenH))  # Background is not draw directly on screen to allow DirtySprite
background.fill((0, 239, 192))  # Our lovely watery color
background = pygame.image.load('Images/test.jpg')

pygame.mouse.set_visible(0)  # (To hide mouse)

# Define number crunching functions ------------------------------------------------------------------------------------


def get_angle(p1, p2):
    xdif = p2[0] - p1[0]
    ydif = p2[1] - p1[1]
    return round(degrees(atan2(ydif, xdif)))


def set_pos(actor, x, y):
    actor.rect.x = x
    actor.rect.y = y


# Setup user interface -------------------------------------------------------------------------------------------------

compass = pygame.image.load("Images/UI/compass.png")
background.blit(compass, (10, 10))

# Setup sprite classes and enemy types ---------------------------------------------------------------------------------


class Simple(pygame.sprite.DirtySprite):  # Layered sprite with image and rect
    def __init__(self, file):
        super().__init__()

        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()


class Normal (pygame.sprite.DirtySprite):  # Layered sprite with sprite sheet and
    def __init__(self, sheet, frames, width, height):
        super().__init__()

        self.xclip = 0
        self.sFrames = frames
        self.sWidth = width
        self.sHeight = height
        self.spritesheet = pygame.image.load(sheet)
        self.spritesheet.set_clip(pygame.Rect(self.xclip, 0, width, height))  # Locate the sprite you want
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.rect = self.image.get_rect()
        self.layer = 0

    timer = 0

    def ani(self):
        self.timer += 1
        if self.timer == 5:
            self.timer = 0

            if self.xclip == (self.sFrames - 1) * self.sWidth:
                self.xclip = 0
            else:
                self.xclip += self.sWidth
            self.dirty = 1
            self.spritesheet.set_clip(pygame.Rect(self.xclip, 0, self.sWidth, self.sHeight))  # Locate sprite
            self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
            self.image = pygame.transform.scale(self.image, (int(self.sWidth * zoom), int(self.sHeight * zoom)))


class CustomMouse(pygame.sprite.DirtySprite):

    def __init__(self, file):
        super().__init__()

        self.img = pygame.image.load(file)
        self.image = self.img
        self.rect = self.image.get_rect()

    def follow(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dirty = 1
        player.image = pygame.transform.scale(player.img, (20, 16))
        player.image = pygame.transform.rotate(player.image, 90 - get_angle(pos, player.rect.center))
        player.dirty = 1

player = CustomMouse('Images/human.png')
player.rect.x = 500
player.rect.y = 300
glacial = Normal('Images/Creatures/glacialPuffer.png', 6, 20, 22)
set_pos(glacial, 400, 720)
prop = Normal('Images/Blocks/prop2.png', 8, 16, 16)
prop.layer = 1
set_pos(prop, 400, 400)
myMouse = CustomMouse('Images/UI/mouse.png')
sub = Simple('Images/Blocks/sub.png')
set_pos(sub, 550, 200)
allSprites = pygame.sprite.LayeredDirty(glacial, myMouse)


#  Define sounds file/create channel manager ---------------------------------------------------------------------------

click = pygame.mixer.Sound('Sounds/click.ogg')
music = pygame.mixer.Sound('Sounds/cascade.ogg')
if not mute:
    soundtrack = music.play()

allSprites.clear(screen, background)


# GAME LOOP ------------------------------------------------------------------------------------------------------------

while running:
    clock.tick(FPS)
    prop.ani()
    glacial.rect.y -= 1
    glacial.dirty = 1
    glacial.ani()
    if glacial.rect.y < -40:
        glacial.rect.y = 740

    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.ACTIVEEVENT:
            if event.state == 3:  # If screen loses focus
                pause = True
                pygame.mixer.pause()
            elif pause and event.state != 3:  # Screen regains focus
                pygame.mixer.unpause()
                pause = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click.play()
            elif event.button == 4 and zoom > 1:
                zoom -= .1
            elif event.button == 5 and zoom < 3:
                zoom += .1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # M is pressed
                if mute:
                    mute = False
                else:
                    mute = True

        elif event.type == pygame.MOUSEMOTION:
            myMouse.follow()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.rect.y -= 1
        myMouse.follow()
    elif keys[pygame.K_s]:
        player.rect.y += 1
        myMouse.follow()
    if keys[pygame.K_d]:
        player.rect.x += 1
        myMouse.follow()
    elif keys[pygame.K_a]:
        player.rect.x -= 1
        myMouse.follow()

    rects = allSprites.draw(screen)
    pygame.display.update(rects)

    #  pygame.display.set_caption('SubCivic ' + str(math.ceil(clock.get_fps())))  # Draw framerate to caption

# Exit Game ------------------------------------------------------------------------------------------------------------

pygame.quit()
