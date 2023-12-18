# This file was created by: Faaris Iqbal
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os
from settings import *

# Setup asset folders - images, sounds, etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

# Player1 class
class Player1(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        # Load player image and set transparency
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2 - 10, HEIGHT/2 + 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def controls(self):
        # Player1 controls
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -3
        if keys[pg.K_d]:
            self.acc.x = 3
        if keys[pg.K_w]:
            self.jump()

    def jump(self):
        # Player1 jump
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        # Update for Player1
        self.acc = vec(0, PLAYER_GRAV)
        self.controls()
        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.pos.x < 0:
            self.pos.x = 15
        if self.pos.y > HEIGHT:
            self.pos.x = HEIGHT - 10
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH - 15
        if self.pos.y < 0:
            self.pos.y = 15

class Bullet(Sprite):
    def __init__(self, player_pos, direction):
        Sprite.__init__(self)
        self.image = pg.Surface((10, 10))  # Adjust the size of the bullet surface
        self.image.fill(RED)  # Set the color of the bullet
        self.rect = self.image.get_rect()

        # Set initial position based on the player's position
        self.rect.center = player_pos

        # Set initial velocity based on the direction
        if direction == "left":
            self.vel = vec(-BULLET_SPEED, 0)
        elif direction == "right":
            self.vel = vec(BULLET_SPEED, 0)

    def update(self):
        # Update bullet position
        self.rect.x += self.vel.x



            
# Player2 class (similar structure to Player1)
class Player2(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        # Load player image and set transparency
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell2.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2 + 60, HEIGHT/2 + 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def controls(self):
        # Player2 controls
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -3
        if keys[pg.K_RIGHT]:
            self.acc.x = 3
        if keys[pg.K_UP]:
            self.jump()

    def jump(self):
        # Player2 jump
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        # Update for Player2
        self.acc = vec(0, PLAYER_GRAV)
        self.controls()
        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.pos.x < 0:
            self.pos.x = 15
        if self.pos.y > HEIGHT:
            self.pos.x = HEIGHT - 10
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH - 15
        if self.pos.y < 0:
            self.pos.y = 15

# Platform class
class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5

    def update(self):
        # Update for moving platforms
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

        
