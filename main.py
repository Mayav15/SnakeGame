import pygame as pg
import numpy as np
from pygame.math import Vector2
import sys, random

pg.init()
pg.mixer.init()
pg.font.init()

title_font = pg.font.Font(None,60)
score_font = pg.font.Font(None,60)

WIDTH, HEIGHT = 1000,1000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FPS = 60

CELL_SIZE = 25
N_CELLS = 30

OFF_SET = 75                                                                                                        # TO GIVE BORDER IN SCREEN

class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]                                                        # STARTING POSITION OF SNAKE
        self.dir = Vector2(1,0)                                                                                     # STARTING DIRECTION OF MOVEMENT

    def draw(self):
        for part in self.body:
            part_box = (OFF_SET+part.x*CELL_SIZE,OFF_SET+part.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)                      # MAKING IT THE SIZE OF A CELL
            pg.draw.rect(screen,GREEN,part_box)
        
    def update(self):
        self.body = self.body[:-1]                                                                                  # REMOVING THE LAST POSITION OF TAIL
        self.body.insert(0,self.body[0]+self.dir)                                                                   # ADDING DIRECTION TO HEAD OF BODY TO GIVE EFFECT OF TURNING
    
    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.dir = Vector2(1,0)

class Food:
    def __init__(self,snake_body):
        self.position = self.random_pos(snake_body)
    
    def draw(self):
        food_box = pg.Rect(OFF_SET+self.position.x*CELL_SIZE,OFF_SET+self.position.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
        pg.draw.rect(screen,RED,food_box)

    def generate_cell(self):
        x = random.randint(0,N_CELLS-1)
        y = random.randint(0,N_CELLS-1)
        return Vector2(x,y)

    def random_pos(self,snake_body):
        position = self.generate_cell()
        while position in snake_body:
            position = self.generate_cell()
        return position

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()
    
    def update(self):
        if self.state == 'RUNNING':
            self.snake.update()
            self.collision()

    def collision(self):
        # CHECKING FOR COLLSION WITH FOOD
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.random_pos(self.snake.body)
            self.snake.body.append(self.snake.body[-1])
            self.score += 1
        # CHECKING IF COLLISION WITH BOUNDARY    
        if self.snake.body[0].x == N_CELLS or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == N_CELLS or self.snake.body[0].y == -1:
            self.game_over()
        # CHECKING COLLISION WITH ITSELF
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()
    
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.random_pos(self.snake.body)
        self.state = 'STOP'
        self.score = 0

screen = pg.display.set_mode((2*OFF_SET+CELL_SIZE*N_CELLS,2*OFF_SET+CELL_SIZE*N_CELLS))
pg.display.set_caption("Snake Game")

clock = pg.time.Clock()

running = True

game = Game()

# CREATING A USER EVENT TO MAKE THE UPDATE OF POSITION OF THE SNAKE SLOWER, OTHERWISE IT WILL UPDATE ACCORDING TO FPS
SNAKE_UPDATE = pg.USEREVENT
pg.time.set_timer(SNAKE_UPDATE,200)

while running:

    clock.tick(FPS)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == SNAKE_UPDATE:                                          # CONDTION TO UPDATE EVERYTIME USER EVENT TRIGGERS
            game.update()
        if event.type == pg.KEYDOWN:
            if game.state == 'STOP':
                game.state = 'RUNNING'
            if event.key == pg.K_UP and game.snake.dir != Vector2(0,1):         # TO CHANGE DIRECTION OF SNAKE BUT NOT TURN 180 IN ONE BUTTON
                game.snake.dir = Vector2(0,-1)
            if event.key == pg.K_DOWN and game.snake.dir != Vector2(0,-1):
                game.snake.dir = Vector2(0,1)
            if event.key == pg.K_RIGHT and game.snake.dir != Vector2(-1,0):
                game.snake.dir = Vector2(1,0)
            if event.key == pg.K_LEFT and game.snake.dir != Vector2(1,0):
                game.snake.dir = Vector2(-1,0)

    screen.fill(BLACK)
    pg.draw.rect(screen,WHITE,(OFF_SET-5,OFF_SET-5,CELL_SIZE*N_CELLS+10,CELL_SIZE*N_CELLS+10),5)
    game.draw()
    title_surface = title_font.render("Snake Game", True, WHITE)
    score_surface = score_font.render("Score:"+str(game.score),True,GREEN)
    screen.blit(title_surface,(OFF_SET-5,20))
    screen.blit(score_surface,(CELL_SIZE*N_CELLS-1.5*OFF_SET,20))

    pg.display.flip()
pg.quit()