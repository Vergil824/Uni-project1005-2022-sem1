# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

from turtle import home
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game
# background coded by wshi9637
# loading a background image for the homescreen
bg = pygame.image.load("bp.png")

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)
Beige = pygame.Color(245, 245, 220)
bright_Beige = pygame.Color(255, 245, 238)
FireBrick = pygame.Color(178, 34, 34)
BurlyWoord = pygame.Color(222, 184, 135)
Moccasin = pygame.Color(255, 228, 181)
Cornsilk = pygame.Color(255, 248, 220)
Tomato = pygame.Color(255, 99, 71)
OrangeRed = pygame.Color(255, 69, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(
    (game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')
home_screen = pygame.mixer.Sound('./sound/homescreen.mp3')
home_screen.set_volume(0.15)
home_screen.play(loops=-1)
# lowering the volume in homescreen


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# function edited by wshi9637


# adjusted the message_display to accept argument relating to text size
def message_display(text, x, y, text_size, color=black):
    if text_size == 'small':
        text_size = pygame.font.Font('./font/Regular.otf', 20)
    else:  # large is default text size
        text_size = pygame.font.Font('./font/Bold.otf', 60)

    text_surf, text_rect = text_objects(text, text_size, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h),
                         border_radius=int(h/2))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color,
                         (x, y, w, h), border_radius=int(h/2))

    smallText = pygame.font.Font('./font/Regular.otf', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15,
                    game.settings.height / 3 * 15, 'large', white)

    time.sleep(2)

# pause feature coded by wshi9637


def pause():
    paused = True
    while paused:  # initiating while loop to check status of pause
        for event in pygame.event.get():  # initiates an event loop
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # unpauses the game
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:  # quits game if user presses q
                    pygame.quit()
                    quit()
        screen.fill(white)
        screen.blit(bg, (0, 0))
        message_display('Paused', game.settings.width / 2 * 15, game.settings.height /
                        4 * 15, 'large', Moccasin)  # informs user game is paused
        message_display("Press C to continue or Q to quit.", game.settings.width / 2 * 15,
                        game.settings.height / 1.4 * 15, 'small', Moccasin)  # informs user of possible actions
        # limiting the tick to 5 as paused screen should be stationary
        fpsClock.tick(5)


def initial_interface():
    intro = True
    pygame.mixer.Sound.play(home_screen)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, black, (game.settings.width / 30 *
                                         15, game.settings.height / 6 * 15, 400, 90), border_radius=20)
        message_display('Gluttonous', game.settings.width / 2 *
                        15, game.settings.height / 4 * 15, 'large', Tomato)
        message_display('Press P to pause', game.settings.width /
                        2 * 15, (game.settings.height / 1.3 * 15), 'small', Tomato)
        message_display(f'Previous highscore: {snake.high_score()}',
                        game.settings.width / 2 * 15, (game.settings.height / 2 * 15) - 60, 'small', Tomato)

        button('Human', 40, 240, 80, 40, BurlyWoord,
               Cornsilk, game_loop, 'human')
        button('Devil', 160, 240, 80, 40, BurlyWoord,
               Cornsilk, game_loop, 'Devil')
        button('Hell', 280, 240, 80, 40, BurlyWoord,
               Cornsilk, game_loop, 'Devil may cry')
        button('Quit', 160, 350, 80, 40, FireBrick, bright_red, quitgame)

        pygame.display.update()
        pygame.time.Clock().tick(3)


def game_loop(player, fps=10):
    game.restart_game()

    while not game.game_end():

        pygame.event.pump()

        move = human_move()
        if player == 'human':
            fps = 5
        elif player == 'Devil':
            fps = 15
        elif player == 'Devil may cry':
            fps = 25

        game.do_move(move)

        screen.fill(black)

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        game.blit_high_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == ord('p'):  # if the user presses p, pause the game
                pause()

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
