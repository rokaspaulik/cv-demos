import pygame
import random
from enum import Enum

class SNAKE_DIRECTION(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# pygame setup
pygame.init()

screen_size = 512
screen_size_zero = 0

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
running = True

step_length = 16

snake_direction = SNAKE_DIRECTION(SNAKE_DIRECTION.RIGHT)

def snake_movement(snake_direction):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake_direction != SNAKE_DIRECTION.DOWN:
        snake_direction = SNAKE_DIRECTION.UP
    if keys[pygame.K_s] and snake_direction != SNAKE_DIRECTION.UP:
        snake_direction = SNAKE_DIRECTION.DOWN
    if keys[pygame.K_a] and snake_direction != SNAKE_DIRECTION.RIGHT:
        snake_direction = SNAKE_DIRECTION.LEFT
    if keys[pygame.K_d] and snake_direction != SNAKE_DIRECTION.LEFT:
        snake_direction = SNAKE_DIRECTION.RIGHT

    match snake_direction:
        case SNAKE_DIRECTION.UP:
            snake_player.pos_y -= step_length
        case SNAKE_DIRECTION.DOWN:
            snake_player.pos_y += step_length
        case SNAKE_DIRECTION.LEFT:
            snake_player.pos_x -= step_length
        case SNAKE_DIRECTION.RIGHT:
            snake_player.pos_x += step_length

    if snake_player.pos_x >= screen_size:
        snake_player.pos_x = screen_size_zero
    if snake_player.pos_x < screen_size_zero:
        snake_player.pos_x = screen_size
    if snake_player.pos_y >= screen_size:
        snake_player.pos_y = screen_size_zero
    if snake_player.pos_y < screen_size_zero:
        snake_player.pos_y = screen_size

    return snake_direction

def spawn_apple():
    random_x = random.randint(1, 31) * 16
    random_y = random.randint(1, 31) * 16

    return Apple(random_x, random_y)

class Apple:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class Snake:
    def __init__(self, pos_x, pos_y, snake_segments):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.snake_segments = snake_segments

class SnakeSegment:
  def __init__(self, pos_x, pos_y, alive_for_ticks):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.alive_for_ticks = alive_for_ticks

# snake with 3 starting segments
snake_player = Snake(256, 256, 3)
snake_segments = []
apple = spawn_apple()

font = pygame.font.Font('freesansbold.ttf', 12) 
text = font.render('SCORE: ' + str(snake_player.snake_segments), True, "green", "black")
textRect = text.get_rect()
textRect.center

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    text = font.render('SCORE: ' + str(snake_player.snake_segments), True, "green", "black")
    screen.blit(text, textRect)

    old_pos_x = snake_player.pos_x
    old_pos_y = snake_player.pos_y

    snake_direction = snake_movement(snake_direction)
    pygame.draw.rect(screen, "green", (snake_player.pos_x, snake_player.pos_y, step_length, step_length))

    new_segment = SnakeSegment(old_pos_x, old_pos_y, snake_player.snake_segments)
    snake_segments.append(new_segment)

    for segment in snake_segments:
        if (snake_player.pos_x == segment.pos_x and snake_player.pos_y == segment.pos_y):
            snake_player = Snake(256, 256, 3)
            snake_segments = []
            apple = spawn_apple()

        segment.alive_for_ticks -= 1
        if (segment.alive_for_ticks == 0):
            snake_segments.remove(segment)
        else:
            pygame.draw.rect(screen, "orange", (segment.pos_x, segment.pos_y, step_length, step_length))

    pygame.draw.rect(screen, "red", (apple.pos_x, apple.pos_y, step_length, step_length))

    if (snake_player.pos_x == apple.pos_x and snake_player.pos_y == apple.pos_y):
        snake_player.snake_segments += 1
        apple = spawn_apple()

    pygame.display.flip()
    clock.tick(20)

pygame.quit()