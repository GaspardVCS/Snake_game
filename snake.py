import pygame
from pygame.math import Vector2
import random
import sys

pygame.init()

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 255), block_rect)
    
    def move_snake(self):
        body_copy = [self.body[0] + self.direction] + self.body[:-1]
        self.body = body_copy[:]
    
    def add_block(self):
        self.body.append(self.body[-1])

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_dead()
    
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_dead(self):
        # Check if snake is outside the screen
        snake_x = self.snake.body[0].x
        snake_y = self.snake.body[0].y
        inside = (0 <= snake_x < cell_number) and (0 <= snake_y < cell_number)
        eat_itself = any(self.snake.body[0] == body_part for body_part in self.snake.body[1:])
        if (not inside) or eat_itself:
            self.game_over()
    
    def game_over(self):
        print("YOU DIE")
        pygame.quit()
        sys.exit

cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150) # this event is going to be trigeerred every 150ms

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)