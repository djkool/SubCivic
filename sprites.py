import pygame

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
            #self.image = pygame.transform.scale(self.image, (int(self.sWidth * zoom), int(self.sHeight * zoom)))


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
        #player.image = pygame.transform.scale(player.img, (20, 16))
        #player.image = pygame.transform.rotate(player.image, 90 - get_angle(pos, player.rect.center))
        #player.dirty = 1
