"""
main.py - Main gamestate that holds all functionality previous provided by the startup script.

"""

import pygame
from gamelib.game import GameState
from math import atan2, degrees

from sprites import *


# Define number crunching functions ------------------------------------------------------------------------------------


def get_angle(p1, p2):
    xdif = p2[0] - p1[0]
    ydif = p2[1] - p1[1]
    return round(degrees(atan2(ydif, xdif)))


def set_pos(actor, x, y):
    actor.rect.x = x
    actor.rect.y = y



# Main State-----------------------------------------------------------------------------------------------------------

class MainState(GameState):

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.zoom = 2
        self.background = None
        self.compass = None
        self.player = None
        self.glacial = None
        self.prop = None
        self.sub = None

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

        # Load State Assets
        #self.background = pygame.Surface((screenW, screenH))  # Background is not draw directly on screen to allow DirtySprite
        #self.background.fill((0, 239, 192))  # Our lovely watery color
        self.background = pygame.image.load('Images/test.jpg')

        # Setup user interface -----------------------------------------------------------------------------------------

        self.compass = pygame.image.load("Images/UI/compass.png")
        self.background.blit(self.compass, (10, 10))

        self.player = CustomMouse('Images/human.png')
        self.player.rect.x = 500
        self.player.rect.y = 300
        self.glacial = Normal('Images/Creatures/glacialPuffer.png', 6, 20, 22)
        set_pos(self.glacial, 400, 720)
        self.prop = Normal('Images/Blocks/prop2.png', 8, 16, 16)
        self.prop.layer = 1
        set_pos(self.prop, 400, 400)

        self.sub = Simple('Images/Blocks/sub.png')
        set_pos(self.sub, 550, 200)
        self.allSprites = pygame.sprite.LayeredDirty(self.glacial, self.gc.mouse)
        self.allSprites.clear(self.gc.screen, self.background)


    def enter(self):
        """Called every time the game is switched to this state."""
        pass

    def processInput(self):
        """Called during normal update/render period for this state
           to process it's input."""

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.gc.quit()

            elif event.type == pygame.ACTIVEEVENT:
                if event.state == 3:  # If screen loses focus
                    self.gc.pause = True
                    pygame.mixer.pause()
                elif self.gc.pause and event.state != 3:  # Screen regains focus
                    pygame.mixer.unpause()
                    self.gc.pause = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #click.play()
                    pass
                elif event.button == 4 and self.zoom > 1:
                    self.zoom -= .1
                elif event.button == 5 and self.zoom < 3:
                    self.zoom += .1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # M is pressed
                    if self.gc.mute:
                        self.gc.mute = False
                    else:
                        self.gc.mute = True

            elif event.type == pygame.MOUSEMOTION:
                self.gc.mouse.follow()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.rect.y -= 1
            self.gc.mouse.follow()
        elif keys[pygame.K_s]:
            self.player.rect.y += 1
            self.gc.mouse.follow()
        if keys[pygame.K_d]:
            self.player.rect.x += 1
            self.gc.mouse.follow()
        elif keys[pygame.K_a]:
            self.player.rect.x -= 1

    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""
        self.prop.ani()
        self.glacial.rect.y -= 1
        self.glacial.dirty = 1
        self.glacial.ani()
        if self.glacial.rect.y < -40:
            self.glacial.rect.y = 740

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        rects = self.allSprites.draw(self.gc.screen)
        pygame.display.update(rects)

# end WorldState
