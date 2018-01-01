import pygame
from pygame.locals import *
import sys
import constants
import random
from main_game import MainGame
from tetrimino_pattern import TetriminoPattern
import util

BLOCK_IMAGE_PATH = 'assets/blocks.png'
BACKGROUND_IMAGE_PATH = 'assets/back_ground.png'
PRESS_ANY_KEY_IMAGE_PATH = 'assets/press_any_key.png'

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
        assets['block_imaeg_list'], assets['background_image'], assets['press_any_key_image'] = load_images()

        while (True):
            clock.tick(60)
            if self.status == constants.STATUS_START_MENU:
                self.__draw_start_menu(screen, assets)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        self.status = constants.STATUS_PLAYING
                        main_game = MainGame(screen, assets)
                    if event.type == QUIT:
                        exit()

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

    def __draw_start_menu(self, screen, assets):
        img_width = assets['background_image'].get_width()
        img_height = assets['background_image'].get_height()
        bgimg = util.scale(assets['background_image'], 2)

        scr_width = screen.get_width()
        scr_height = screen.get_height()
        for x in range(int(scr_width / (img_width * 2))):
            for y in range(int(scr_height / (img_height * 2))):
                screen.blit(bgimg, (x * img_width * 2, y * img_height * 2))

        press_ak_img =util.scale(assets['press_any_key_image'], 2)
        screen.blit(press_ak_img, (0, 4 * 10 * 2))

def load_images():
    block_num = 7
    block_width = 10
    block_height = 10

    all_blocks_image = pygame.image.load(BLOCK_IMAGE_PATH).convert()
    block_image_list = []
    for i in range(block_num):
        shape = Rect(0, i * block_height, block_width, block_height)
        block_image_list.append(all_blocks_image.subsurface(shape))

    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
    press_any_key_image = pygame.image.load(PRESS_ANY_KEY_IMAGE_PATH).convert()

    return [block_image_list, background_image, press_any_key_image]
