import random
import copy
import pygame
from pygame.locals import *
from field import Field
from tetrimino import Tetrimino

class MainGame:
    KEY_NOT_PRESSED = 0
    KEY_PRESSED = 1
    KEY_HOLDING_PRESSED = 2

    def __init__(self, screen, assets):
        self.should_generate_tetrimino = True
        self.should_decide_deleting_blocks = False
        self.is_gameover = False
        self.prior_key_states = [MainGame.KEY_NOT_PRESSED] * 323
        self.screen = screen

        self.next_tetrimino_type = random.randint(0, 6)
        self.assets = assets
        self.field = Field()
        self.frames_to_fall = 60

    def step_frame(self):
        if self.should_generate_tetrimino:
            succeeded_tetrimino = self.__try_generate_tetrimino()
            if not succeeded_tetrimino:
                self.is_gameover = True
                return
            self.should_generate_tetrimino = False

        self.__control_tetrimino()
        if self.frames_to_fall <= 0:
            self.__try_drop_tetrimino(self.tetrimino, self.field)

        #if self.should:
        #    self.__delete_blocks()

        self.frames_to_fall -= 1
        self.__draw()

    def is_gameover(self):
        return self.is_gameover

    def __try_generate_tetrimino(self):
        self.tetrimino = Tetrimino(self.next_tetrimino_type)
        self.next_tetrimino_type = random.randint(0, 6)

        is_generatable = self.__determine_generatability(self.field, self.tetrimino)
        if not is_generatable:
            return False

        return True

    def __determine_generatability(self, field, tetrimino):
        tetrimino_blocks = tetrimino.generate_blocks_as_field_format()
        for y in range(Field.HEIGHT):
            for x in range(Field.WIDTH):
                if field.get_block(x, y) is not None and tetrimino_blocks[y][x] is not None:
                    return False
        return True

    def __control_tetrimino(self):
        keys = self.__get_key_status()
        if keys[pygame.K_UP] == MainGame.KEY_PRESSED:
            self.__try_rotate(self.tetrimino)
        if keys[pygame.K_DOWN] == MainGame.KEY_PRESSED:
            self.__try_drop_tetrimino(self.tetrimino, self.field)
        if keys[pygame.K_LEFT] == MainGame.KEY_PRESSED:
            self.__try_move_tetrimino(self.tetrimino, Tetrimino.LEFT)
        if keys[pygame.K_RIGHT] == MainGame.KEY_PRESSED:
            self.__try_move_tetrimino(self.tetrimino, Tetrimino.RIGHT)

    def __get_key_status(self):
        def get_key_val(key, prior_key):
            if key == 0:
                return MainGame.KEY_NOT_PRESSED
            elif key == 1 and prior_key == MainGame.KEY_NOT_PRESSED:
                return MainGame.KEY_PRESSED
            else:
                return MainGame.KEY_HOLDING_PRESSED

        keys = pygame.key.get_pressed()
        key_detail = [get_key_val(k, pk) for (k, pk) in zip(keys, self.prior_key_states)]
        self.prior_key_states = key_detail
        return key_detail

    def __try_rotate(self, tetrimino):
        def determine_rotatability(tetrimino, field):
            ghost_tetrimino = copy.deepcopy(tetrimino)
            ghost_tetrimino.rotate()
            blocks = ghost_tetrimino.generate_blocks_as_coodinate_array()
            for block in blocks:
                if block[0] < 0 or block[0] >= Field.WIDTH:
                    return False
                if block[1] < 0 or block[1] >= Field.HEIGHT:
                    return False
                if field.get_block(block[0], block[1]) != None:
                    return False
            return True

        is_rotatable = determine_rotatability(tetrimino, self.field)
        if is_rotatable:
            tetrimino.rotate()

    def __try_move_tetrimino(self, tetrimino, direction):
        def determine_movabimitly(tetrimino, field, direction):
            ghost_tetrimino = copy.deepcopy(tetrimino)
            ghost_tetrimino.move(direction)
            blocks = ghost_tetrimino.generate_blocks_as_coodinate_array()
            for block in blocks:
                if block[0] < 0 or block[0] >= Field.WIDTH:
                    return False
                if block[1] < 0 or block[1] >= Field.HEIGHT:
                    return False
                if field.get_block(block[0], block[1]) != None:
                    return False
            return True

        is_movable = determine_movabimitly(tetrimino, self.field, direction)
        if is_movable:
            tetrimino.move(direction)

    def __try_drop_tetrimino(self, tetrimino, field):
        def determin_droppability(tetrimino, field):
            ghost_tetrimino = copy.deepcopy(tetrimino)
            ghost_tetrimino.fall()
            blocks = ghost_tetrimino.generate_blocks_as_coodinate_array()
            for block in blocks:
                if block[0] < 0 or block[0] >= Field.WIDTH:
                    return False
                if block[1] < 0 or block[1] >= Field.HEIGHT:
                    return False
                if field.get_block(block[0], block[1]) != None:
                    return False
            return True

        is_droppable = determin_droppability(tetrimino, field)
        if is_droppable:
            tetrimino.fall()
        else:
            self.__fix_blocks(tetrimino, field)
        self.frames_to_fall = 60

    def __fix_blocks(self, tetrimino, field):
        tetrimino_blocks = tetrimino.generate_blocks_as_coodinate_array()
        block_color = tetrimino.tetrimino_type

        for block in tetrimino_blocks:
            field.set_block(block[0], block[1], block_color)

        field.try_delete_blocks()

        self.should_generate_tetrimino = True

    def __draw(self):
        self.screen.fill((255,255,255))
        self.field.draw(self.screen)
        self.tetrimino.draw(self.screen)
