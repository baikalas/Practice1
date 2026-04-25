import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 800))

pygame.draw.circle(screen, (255, 255, 255), (500, 400), 300, width=5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()