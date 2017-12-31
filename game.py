import pygame
from pygame.locals import *
import sys
import constants
import random
from main_game import MainGame
from tetrimino_pattern import TetriminoPattern

class Game:
    def __init__(self):
        self.status = constants.STATUS_START_MENU

    def run(self):
        assets = {}
        assets['tetrimino_pattern'] = TetriminoPattern()
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((400, 480))
        pygame.display.set_caption("Test")

        while (True):
            clock.tick(60)
            if self.status == constants.STATUS_START_MENU:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        self.status = constants.STATUS_PLAYING
                        main_game = MainGame(screen, assets)

            elif self.status == constants.STATUS_PLAYING:
                main_game.step_frame()
                if main_game.is_gameover:
                    self.status = constants.STATUS_GAMEOVER

            elif self.status == constants.STATUS_GAMEOVER:
                screen.fill((255,255,255))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

def get_key_status():
    if key == pygame.K_UP:
        print()
        color += 24
    elif key == pygame.K_DOWN:
        color -= 24
