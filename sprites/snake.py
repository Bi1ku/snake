import pygame as pg


class Snake (pg.sprite.Sprite):
    def __init__(self, x = 100, y = 300, direction = "RIGHT"):
        super().__init__()
        self.image = pg.Surface([20, 20])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.direction = direction

    def move(self):
        if self.direction == "RIGHT":
            self.rect.x += 20
        elif self.direction == "LEFT":
            self.rect.x -= 20
        elif self.direction == "UP":
            self.rect.y -= 20
        elif self.direction == "DOWN":
            self.rect.y += 20

    def update(self):
        self.move()
