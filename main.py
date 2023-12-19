# Import necessary libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math

# This file was created by: Faaris Iqbal
# Content from Chris Bradfield; Kids Can Code
# Logo image source: https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2FDwayneJohnson%2Fphotos%2Fa.448580834383%2F10154509349039384%2F%3Ftype%3D3
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0

# Title: gun arena

'''
Goals:
Make an arena with platforms
Make two characters with guns
If other person is shot, the game ends
They also have a melee they can use if close enough
'''

# Define a vector
vec = pg.math.Vector2

p1win = False
p2win = False

# Set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')
class Cooldown:
    def __init__(self):
        self.last_shot_time = 0
        self.cooldown_duration = 0.3

    def can_shoot(self):
        current_time = pg.time.get_ticks() / 1000
        time_since_last_shot = current_time - self.last_shot_time
        return time_since_last_shot >= self.cooldown_duration

    def update_last_shot_time(self):
        self.last_shot_time = pg.time.get_ticks() / 1000




cd = Cooldown()


# Game class
class Game:
    def __init__(self):
        self.cooldown = Cooldown()
        self.p1_won = False
        self.p2_won = False
        self.cooldown_p1 = Cooldown()
        self.cooldown_p2 = Cooldown()
        # Initialize pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.start_time = pg.time.get_ticks()
        self.all_bullets = pg.sprite.Group()  # Initialize the all_bullets group here


    def new(self):
        # Create a group for all sprites
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        # Instantiate player classes
        self.player1 = Player1(self)
        self.player2 = Player2(self)

        # Add player instances to groups
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        # Reset the start time when starting a new game
        self.start_time = pg.time.get_ticks()

        # Create platforms
        for p in PLATFORM_LIST:
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        self.run()

    def draw_text(self, text, size, color, x, y):
        # Draw text on the screen
        font = pg.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    def run(self):
        # Game loop
        self.playing = True
        game_over = False
        while self.playing and not game_over:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

            # Check for player wins
            if self.player2.rect.y > HEIGHT and not self.p1_won:
                self.p1_won = True
                self.p1_survival_time = (pg.time.get_ticks() - self.start_time) // 1000
                print("p1 win")
                game_over = True
            if self.player1.rect.y > HEIGHT and not self.p2_won:
                self.p2_won = True
                self.p2_survival_time = (pg.time.get_ticks() - self.start_time) // 1000
                print("p2 win")
                game_over = True

        # Display win screen
        elapsed_time = (pg.time.get_ticks() - self.start_time) // 1000
        if self.p1_won:
            self.draw_text(f"Player 1 has won! Survived for {elapsed_time}s", 20, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
        elif self.p2_won:
            self.draw_text(f"Player 2 has won! Survived for {elapsed_time}s", 20, WHITE, WIDTH // 2 - 100, HEIGHT // 2)

        pg.display.flip()
        pg.time.wait(5000)  # Wait for 5 seconds

        # Quit pygame
        pg.quit()


    def update(self):
        # Update all sprites
        self.all_sprites.update()

        # Prevent player from falling through the platform
        if self.player1.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player1, self.all_platforms, False)
            if hits:
                self.player1.pos.y = hits[0].rect.top
                self.player1.vel.y = 0
                self.player1.vel.x = hits[0].speed * 1.5

        if self.player2.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player2, self.all_platforms, False)
            if hits:
                self.player2.pos.y = hits[0].rect.top
                self.player2.vel.y = 0
                self.player2.vel.x = hits[0].speed * 1.5

    def draw(self):
        # Draw the game screen
        self.screen.fill(BLACK)
        elapsed_time = (pg.time.get_ticks() - self.start_time) // 1000
        self.draw_text(f"Time: {elapsed_time}s", 30, WHITE, WIDTH // 2 - 43, 10)
        self.all_sprites.draw(self.screen)

        pg.display.flip()
    def shoot(self, player, bullet_class):
        if player.__class__.__name__ == "Player1" and self.cooldown_p1.can_shoot():
            print(f"{player.__class__.__name__} shooting")
            bullet = bullet_class(player.pos, player.direction)
            self.all_sprites.add(bullet)
            self.all_bullets.add(bullet)
            self.cooldown_p1.update_last_shot_time()
        elif player.__class__.__name__ == "Player2" and self.cooldown_p2.can_shoot():
            print(f"{player.__class__.__name__} shooting")
            bullet = bullet_class(player.pos, player.direction)
            self.all_sprites.add(bullet)
            self.all_bullets.add(bullet)
            self.cooldown_p2.update_last_shot_time()

    def events(self):
        # Handle game events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # Handle key presses
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.shoot(self.player1, Bullet1)  # Pass Bullet1 for Player1
                elif event.key == pg.K_RETURN:
                    self.shoot(self.player2, Bullet2)  # Pass Bullet2 for Player2

            # Handle key releases (remove the KEYUP part if not needed)
            if event.type == pg.KEYUP:
                if event.key in [pg.K_SPACE, pg.K_RETURN]:
                    # You can choose to do something here if needed
                    pass
    def show_start_screen(self):
        # Display the start screen
        pass

    def show_go_screen(self):
        # Display the game over screen
        pass


# Game loop
gamerun = True
g = Game()
while gamerun:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    g.new()
    g.shoot()
# Quit pygame
pg.quit()
