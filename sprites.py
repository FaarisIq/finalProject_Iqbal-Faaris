# This file was created by: Faaris Iqbal
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

import pygame as pg
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
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
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
            self.acc.x = -5
        if keys[pg.K_RIGHT]:
            self.acc.x = 5
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

# Mob1 class (similar structure to Mob2)
class Mob1(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, 400)
        self.mobspeedx = 1
        self.mobspeedy = 1
        self.acceleration = 0.0035  # Adjust the acceleration rate as needed

    def update(self):
        # Update for Mob1
        if self.game.player1.rect.colliderect(self.rect):
            self.game.p1_won = False
            self.game.p2_won = True
            self.game.playing = False
        if self.game.player1.rect.x > self.rect.x:
            self.rect.x += self.mobspeedx
            self.mobspeedx += self.acceleration
        elif self.game.player1.rect.x < self.rect.x:
            self.rect.x -= self.mobspeedx
            self.mobspeedx += self.acceleration

        if self.game.player1.rect.y > self.rect.y:
            self.rect.y += self.mobspeedy
            self.mobspeedy += self.acceleration
        elif self.game.player1.rect.y < self.rect.y:
            self.rect.y -= self.mobspeedy
            self.mobspeedy += self.acceleration
        if self.mobspeedy == self.game.player1.rect.y + 1 or self.mobspeedy == self.game.player1.rect.y - 1 and self.mobspeedx == self.game.player1.rect.x + 1 or self.mobspeedx == self.game.player1.rect.x - 1:
            self.acceleration = 0

# Mob2 class
class Mob2(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(DARKGREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, 400)
        self.mobspeedx = 1
        self.mobspeedy = 1
        self.acceleration = 0.005  # Adjust the acceleration rate as needed

    def update(self):
        # Update for Mob2
        if self.game.player2.rect.colliderect(self.rect):
            self.game.p1_won = True
            self.game.p2_won = False
            self.game.playing = False
        if self.game.player2.rect.x > self.rect.x:
            self.rect.x += self.mobspeedx
            self.mobspeedx += self.acceleration
        elif self.game.player2.rect.x < self.rect.x:
            self.rect.x -= self.mobspeedx
            self.mobspeedx += self.acceleration

        if self.game.player2.rect.y > self.rect.y:
            self.rect.y += self.mobspeedy
            self.mobspeedy += self.acceleration
        elif self.game.player2.rect.y < self.rect.y:
            self.rect.y -= self.mobspeedy
            self.mobspeedy += self.acceleration
        if self.mobspeedy == self.game.player1.rect.y + 1 or self.mobspeedy == self.game.player1.rect.y - 1 and self.mobspeedx == self.game.player1.rect.x + 1 or self.mobspeedx == self.game.player1.rect.x - 1:
            self.acceleration = 0
