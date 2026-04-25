import pygame
import sys
import random

pygame.init()

# -------- SETTINGS -------- #
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Grid size
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)

# -------- GAME VARIABLES -------- #
snake = [(10, 10)]
direction = (1, 0)

food = None
walls = set()

score = 0
level = 1
speed = 8

# -------- CREATE WALLS -------- #
# Border walls
for x in range(COLS):
    walls.add((x, 0))
    walls.add((x, ROWS - 1))

for y in range(ROWS):
    walls.add((0, y))
    walls.add((COLS - 1, y))


# -------- FUNCTIONS -------- #

def generate_food():
    """Generate food not on snake or walls"""
    while True:
        pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
        if pos not in snake and pos not in walls:
            return pos


def draw_cell(pos, color):
    """Draw a single grid cell"""
    rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def draw_text():
    """Draw score and level"""
    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))


def next_level():
    """Increase level and speed"""
    global level, speed
    level += 1
    speed += 2


# First food spawn
food = generate_food()


# -------- GAME LOOP -------- #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # -------- MOVE SNAKE -------- #
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # -------- COLLISIONS -------- #

    # Wall collision OR leaving area
    if new_head in walls or \
       new_head[0] < 0 or new_head[0] >= COLS or \
       new_head[1] < 0 or new_head[1] >= ROWS:
        print("Game Over: hit wall")
        pygame.quit()
        sys.exit()

    # Self collision
    if new_head in snake:
        print("Game Over: ate yourself")
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # -------- FOOD -------- #
    if new_head == food:
        score += 1
        food = generate_food()

        # Level up every 4 points
        if score % 4 == 0:
            next_level()
    else:
        snake.pop()

    # -------- DRAW -------- #
    screen.fill(WHITE)

    # Draw walls
    for w in walls:
        draw_cell(w, BLACK)

    # Draw snake
    for segment in snake:
        draw_cell(segment, GREEN)

    # Draw food
    draw_cell(food, RED)

    # Draw UI
    draw_text()

    pygame.display.update()
    clock.tick(speed)