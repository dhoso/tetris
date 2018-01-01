import random
import copy
import pygame
from pygame.locals import *
from field import Field
from tetrimino import Tetrimino
import util

class MainGame:
    KEY_NOT_PRESSED = 0
    KEY_PRESSED = 1
    KEY_HOLDING_PRESSED = 2

    def __init__(self, screen, assets):
        self.should_generate_tetrimino = True
        self.should_decide_deleting_blocks = False
        self.is_gameover = False
        self.is_finished = False
        self.prior_key_states = [MainGame.KEY_NOT_PRESSED] * 323
        self.screen = screen

        self.next_tetrimino_type = random.randint(0, 6)
        self.assets = assets
        self.field = Field(self.assets)
        self.initial_frames_to_fall = 60
        self.frames_to_fall = self.initial_frames_to_fall
        self.score = 0
        self.fixing_block_count = 0

    def step_frame(self):
        if self.is_gameover:
            self.__gameover()
            return

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
        self.tetrimino = Tetrimino(self.next_tetrimino_type, self.assets)
        self.next_tetrimino_type = random.randint(0, 6)
        self.next_tetrimino_for_preview = Tetrimino(self.next_tetrimino_type, self.assets)
        self.next_tetrimino_for_preview.set_base((1, 1))

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
        self.frames_to_fall = self.initial_frames_to_fall

    def __fix_blocks(self, tetrimino, field):
        tetrimino_blocks = tetrimino.generate_blocks_as_coodinate_array()
        block_color = tetrimino.tetrimino_type

        for block in tetrimino_blocks:
            field.set_block(block[0], block[1], block_color)

        self.score += field.try_delete_blocks()
        self.fixing_block_count += 1
        if self.fixing_block_count % (600 / self.initial_frames_to_fall) == 0:
            self.initial_frames_to_fall = max(int(self.initial_frames_to_fall * 3 / 4), 1)

        self.should_generate_tetrimino = True

    def __draw(self):
        block_size = 10
        scale = 2

        def draw_background_surface():
            width = self.screen.get_width()
            height = self.screen.get_height()

            surface = pygame.Surface((width, height))
            background_scaled = pygame.transform.scale(self.assets['background_image'], (block_size * scale, block_size * scale))
            for x in range(int(width / (block_size * scale))):
                for y in range(int(height / (block_size * scale))):
                    surface.blit(background_scaled, (x * block_size * scale, y * block_size * scale))
            return surface

        def draw_game_field_surface():
            surface_on_field = pygame.Surface((Field.WIDTH * block_size, Field.HEIGHT * block_size))
            self.field.draw(surface_on_field)
            self.tetrimino.draw(surface_on_field)
            dst_size = (surface_on_field.get_width() * scale, surface_on_field.get_height() * scale)
            return pygame.transform.scale(surface_on_field, dst_size)

        def draw_next_tetrimino_preview_surface():
            preview_block_width = 5
            preview_block_height = 5
            width = preview_block_width * block_size
            height = preview_block_height * block_size

            surface = pygame.Surface((width, height))
            surface.fill((0, 0, 0))
            self.next_tetrimino_for_preview.draw(surface)
            return pygame.transform.scale(surface, (width * scale, height * scale))

        def draw_score_surface(score):
            score_str = str(score)
            letter_width, letter_height = self.assets['number_image_list'][0].get_size()
            score_width, score_height = self.assets['score_image'].get_size()
            bg_width, bg_height = self.assets['score_background_image'].get_size()
            surface_width = bg_width
            surface_height = bg_height

            surface = pygame.Surface((surface_width , surface_height))
            surface.blit(self.assets['score_background_image'], (0, 0))

            surface.blit(self.assets['score_image'], (0, 0))

            for i, letter in enumerate(score_str):
                surface.blit(self.assets['number_image_list'][int(letter)], (i * letter_width, score_height))
            return surface

        self.screen.blit(draw_background_surface(), (0, 0))
        self.screen.blit(draw_game_field_surface(), (40, 40))
        self.screen.blit(draw_next_tetrimino_preview_surface(), (block_size * scale * 14, block_size * scale * 2))
        score_surface = util.scale(draw_score_surface(self.score), 2)
        self.screen.blit(score_surface, (block_size * scale * 13, block_size * scale * 12))

    def __gameover(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.is_finished = True
        self.__draw()
        self.screen.blit(util.scale(self.assets['gameover_image'], 2), (0, 60))
