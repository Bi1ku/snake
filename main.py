from random import choice
import pygame as pg
from sprites.snake import Snake
from sprites.apple import Apple


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600


def main():
    pg.init()

    def movement_direction(coord1, coord2):
        if coord1[0] < coord2[0]:
            return "LEFT"
        elif coord1[0] > coord2[0]:
            return "RIGHT"
        elif coord1[1] < coord2[1]:
            return "UP"
        elif coord1[1] > coord2[1]:
            return "DOWN"

    def new_snake_pos(previous_coord, direction):
        if direction == "RIGHT":
            return (previous_coord[0] - 20, previous_coord[1])
        elif direction == "LEFT":
            return (previous_coord[0] + 20, previous_coord[1])
        elif direction == "UP":
            return (previous_coord[0], previous_coord[1] + 20)
        elif direction == "DOWN":
            return (previous_coord[0], previous_coord[1] - 20)

    def filter_snake_pos(compared_arr, axis):
        # Deep copy compared_arr to make changes while not referencing the original array
        # In python, arrays are passed by reference, so simply declaring another variable equal to compared_arr
        # would not work because changes to said variable would still affect the original array
        output = compared_arr.copy()
        for pos in list(map(lambda x: x.rect.topleft, snake_blocks.sprites())):
            if pos[axis] in output:
                output.remove(pos[axis])
        return output

    global SCREEN, CLOCK
    game_active = False

    TITLE = pg.font.Font("font/ARCADECLASSIC.TTF",
                         100).render("SNAKE", True, WHITE)
    TITLE_RECT = TITLE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    DESCRIPTION = pg.font.Font(
        "font/ARCADECLASSIC.TTF", 50).render("Press   SPACE   to   start", True, WHITE)
    DESCRIPTION_RECT = DESCRIPTION.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 230))

    score = 0

    SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pg.time.Clock()

    SNAKE_LOGO = pg.image.load(
        "assets/snake_logo.jpeg").convert_alpha()
    SNAKE_LOGO_RECT = SNAKE_LOGO.get_rect(
        center=(WINDOW_HEIGHT/2, WINDOW_WIDTH/2))

    snake_blocks = pg.sprite.Group(Snake())

    APPLE_X_POSITIONS = [x * 20 for x in range(WINDOW_WIDTH//20)]
    APPLE_Y_POSITIONS = [y * 20 for y in range(WINDOW_HEIGHT//20)]
    apple = pg.sprite.GroupSingle(
        Apple(choice(APPLE_X_POSITIONS), choice(APPLE_Y_POSITIONS)))

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not game_active:
                game_active = True

        if game_active:
            SCREEN.fill((0, 0, 0))
            snake_blocks.draw(SCREEN)
            apple.draw(SCREEN)
            drawGrid()

            snake_block_sprites = snake_blocks.sprites()
            total_idx_snake_blocks = len(snake_block_sprites) - 1
            HEAD = snake_block_sprites[0]

            # Input detection (ONLY FOR HEAD SNAKE BLOCK)
            # Outside of event loop due to fast key presses causing snake to move left when moving right, up when moving down, and etc.
            key = pg.key.get_pressed()
            if key[pg.K_RIGHT] and HEAD.direction != "LEFT":
                HEAD.direction = "RIGHT"
            elif key[pg.K_LEFT] and HEAD.direction != "RIGHT":
                HEAD.direction = "LEFT"
            elif key[pg.K_UP] and HEAD.direction != "DOWN":
                HEAD.direction = "UP"
            elif key[pg.K_DOWN] and HEAD.direction != "UP":
                HEAD.direction = "DOWN"

            # Individual snake block movement
            for index in range(1, total_idx_snake_blocks + 1):
                snake_block_sprites[index].direction = movement_direction(
                    snake_block_sprites[index - 1].rect.topleft, snake_block_sprites[index].rect.topleft)

            # Apple collision detection & logic
            if pg.sprite.spritecollide(apple.sprite, snake_blocks, False):
                pos = new_snake_pos(
                    snake_block_sprites[total_idx_snake_blocks].rect.topleft, snake_block_sprites[total_idx_snake_blocks].direction)
                snake_blocks.add(
                    Snake(pos[0], pos[1], snake_block_sprites[total_idx_snake_blocks].direction))
                apple.sprite.change_pos(
                    choice(filter_snake_pos(APPLE_X_POSITIONS, 0)), choice(filter_snake_pos(APPLE_Y_POSITIONS, 1)))

            # Game over detection & logic
            if HEAD.rect.bottom > WINDOW_HEIGHT or HEAD.rect.top < 0 or HEAD.rect.left < 0 or HEAD.rect.right > WINDOW_WIDTH or pg.sprite.spritecollide(HEAD, snake_block_sprites[4:], False):
                snake_blocks.empty()
                snake_blocks = pg.sprite.Group(Snake())
                apple = pg.sprite.GroupSingle(
                    Apple(choice(APPLE_X_POSITIONS), choice(APPLE_Y_POSITIONS)))
                SCREEN.fill(BLACK)
                score = total_idx_snake_blocks
                game_active = False

            snake_blocks.update()

        else:
            score_text = pg.font.Font(
                "font/ARCADECLASSIC.TTF", 50).render(f'Score   {score}', True, WHITE)
            SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_RECT)
            SCREEN.blit(TITLE, TITLE_RECT)
            SCREEN.blit(DESCRIPTION, DESCRIPTION_RECT)
            SCREEN.blit(score_text, score_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 230)))

        pg.display.update()
        CLOCK.tick(10)


def drawGrid():
    BLOCKSIZE = 20
    for x in range(WINDOW_WIDTH // BLOCKSIZE):
        for y in range(WINDOW_HEIGHT // BLOCKSIZE):
            rect = pg.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                           BLOCKSIZE, BLOCKSIZE)
            pg.draw.rect(SCREEN, WHITE, rect, 1)


if __name__ == '__main__':
    main()
