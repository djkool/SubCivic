"""
SubCivic, a submarine simulation, mining, and exploration game. Created by Wesley Barlow & Daniel Reis, 2016.
Writen in Python 3.5 and Pygame 1.9, feel free to learn, mod, or contribute. Party on.

Convert to .EXE file on Mac using PyInstaller
Run the following commands in Terminal
python3.5 -m pip install pyinstaller
open /Users/Wesxdz/PycharmProjects/SubCivic
pyinstaller starup.py
"""

import pygame
from gamelib.game import GameClass
from sprites import CustomMouse

# Game Class -----------------------------------------------------------------------------------------------------------

class SubCivicGame(GameClass):

    def __init__(self):
        GameClass.__init__(self)

        # Global Constants
        self.SCREEN_SIZE = (1280, 720) # Default resolution of FTL and Shiprekt, some users may not have high enough display res though
        self.DESIRED_FPS = 60 # Limit to 30?

        # Itemize Global GameClass variables for reference
        # Anything here can be accessed in a GameState by self.gc.****
        self.screen = None
        self.clock = None
        self.time = 0
        self.time_step = 0.0

        self.pause = False
        self.mute = False

    def initialize(self):
        GameClass.initialize(self)

        # Init pygame
        pygame.init()
        pygame.display.set_caption('SubCivic')  # Set window title (Doesn't work for Mac icon hover?)
        pygame.display.set_icon(pygame.image.load('Images/UI/compass.png'))  # Game icon, 32x32
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.HWSURFACE)
        # ,pygame.FULLSCREEN (To start in fullscreen)
        pygame.mouse.set_visible(0)  # (To hide mouse)
        self.clock = pygame.time.Clock()

        self.mouse = CustomMouse('Images/UI/mouse.png')

        # Load any assets they will be used by all/most game states

        #click = pygame.mixer.Sound('Sounds/click.ogg')
        #music = pygame.mixer.Sound('Sounds/cascade.ogg')
        #if not mute:
        #    soundtrack = music.play()

    def update(self):
        # Must be done before GameClass.update() so it can
        # be used by GameState this frame
        self.clock.tick(self.DESIRED_FPS)
        self.time = pygame.time.get_ticks()
        self.time_step = self.clock.get_time()/1000.0

        GameClass.update(self)

    def shutdown(self):
        GameClass.shutdown(self)
        pygame.quit()

    def quit(self):
        # tell systems to shut down
        self.running = False

# end SubCivicGame


# Initialize Game ------------------------------------------------------------------------------------------------------

game = SubCivicGame()
game.initialize()

# Start first state
from states.main import MainState
game.changeState(MainState)

# GAME LOOP ------------------------------------------------------------------------------------------------------------

while game.running:
    game.update()

# Exit Game ------------------------------------------------------------------------------------------------------------

game.shutdown()
