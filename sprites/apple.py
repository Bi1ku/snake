from secrets import choice
import pygame as pg


class Apple(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (x, y))

    def change_pos(self, new_x_pos, new_y_pos):
        self.rect.topleft = (new_x_pos, new_y_pos)