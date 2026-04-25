import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

ball_pos = [500, 400]
RADIUS = 50

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball_pos[0] -= 10
            elif event.key == pygame.K_RIGHT:
                ball_pos[0] += 10
            elif event.key == pygame.K_UP:
                ball_pos[1] -= 10
            elif event.key == pygame.K_DOWN:
                ball_pos[1] += 10

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), ball_pos, RADIUS)

    pygame.display.flip()
    clock.tick(360)  