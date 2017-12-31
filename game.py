import pygame
from pygame.locals import *
import sys
import constants
import random
from main_game import MainGame
from tetrimino_pattern import TetriminoPattern

BLOCK_IMAGE_PATH = 'assets/blocks.png'

class Game:
    def __init__(self):
        self.status = constants.STATUS_START_MENU

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((400, 480))
        pygame.display.set_caption("Test")

        assets = {}
        assets['tetrimino_pattern'] = TetriminoPattern()
        assets['block_imaeg_list'] = load_images()

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

def load_images():
    block_num = 7
    block_width = 10
    block_height = 10

    all_blocks_image = pygame.image.load(BLOCK_IMAGE_PATH).convert()
    block_image_list = []
    for i in range(block_num):
        shape = Rect(0, i * block_height, block_width, block_height)
        block_image_list.append(all_blocks_image.subsurface(shape))

    return block_image_list
