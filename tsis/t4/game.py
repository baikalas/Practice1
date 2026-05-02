import pygame, random
from config import *
from db import save_game, get_best

class Game:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.reset()

    def reset(self):
        self.snake = [(10, 10)]
        self.direction = (1, 0)

        self.score = 0
        self.level = 1
        self.speed = 8

        self.food = self.spawn()
        self.poison = self.spawn()

        self.walls = set()
        self.make_border()

        self.powerup = None
        self.power_type = None
        self.spawn_time = 0
        self.effect_end = 0
        self.shield = False

        self.best = get_best(self.username)

    def make_border(self):
        for x in range(COLS):
            self.walls.add((x, 0))
            self.walls.add((x, ROWS-1))
        for y in range(ROWS):
            self.walls.add((0, y))
            self.walls.add((COLS-1, y))

    def spawn(self):
        while True:
            pos = (random.randint(1, COLS-2), random.randint(1, ROWS-2))
            if pos not in self.snake:
                return pos

    def draw_cell(self, pos, color):
        r = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, r)

    def update(self):
        head = self.snake[0]
        new = (head[0]+self.direction[0], head[1]+self.direction[1])

        # collision
        if new in self.walls or new in self.snake:
            if self.shield:
                self.shield = False
            else:
                return False

        self.snake.insert(0, new)

        # food
        if new == self.food:
            self.score += 1
            self.food = self.spawn()
            if self.score % 4 == 0:
                self.level += 1
                self.speed += 2
        else:
            self.snake.pop()

        # poison
        if new == self.poison:
            if len(self.snake) <= 2:
                return False
            self.snake = self.snake[:-2]
            self.poison = self.spawn()

        # powerup spawn
        if not self.powerup and random.randint(0,100) < 2:
            self.powerup = self.spawn()
            self.power_type = random.choice(["speed","slow","shield"])
            self.spawn_time = pygame.time.get_ticks()

        # powerup expire
        if self.powerup and pygame.time.get_ticks()-self.spawn_time > 8000:
            self.powerup = None

        # collect powerup
        if new == self.powerup:
            if self.power_type == "speed":
                self.speed += 5
                self.effect_end = pygame.time.get_ticks()+5000
            elif self.power_type == "slow":
                self.speed = max(3, self.speed-3)
                self.effect_end = pygame.time.get_ticks()+5000
            elif self.power_type == "shield":
                self.shield = True
            self.powerup = None

        if self.effect_end and pygame.time.get_ticks()>self.effect_end:
            self.speed = 8 + self.level*2
            self.effect_end = 0

        return True

    def draw(self):
        self.screen.fill(WHITE)

        for w in self.walls:
            self.draw_cell(w, BLACK)

        for s in self.snake:
            self.draw_cell(s, GREEN)

        self.draw_cell(self.food, RED)
        self.draw_cell(self.poison, POISON_COLOR)

        if self.powerup:
            self.draw_cell(self.powerup, (0,0,255))

        font = pygame.font.SysFont("Arial", 20)
        txt = font.render(f"Score:{self.score} Level:{self.level} Best:{self.best}", True, BLACK)
        self.screen.blit(txt,(10,10))