import pygame, sys
from game import Game
from config import *
from db import save_game, get_top10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)

def get_username():
    name = ""
    while True:
        screen.fill(WHITE)
        txt = font.render("Enter Username: "+name, True, BLACK)
        screen.blit(txt,(50,250))

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode

        pygame.display.update()

def show_leaderboard():
    data = get_top10()
    while True:
        screen.fill(WHITE)
        y = 50
        for i,row in enumerate(data):
            txt = font.render(f"{i+1}. {row[0]} {row[1]}", True, BLACK)
            screen.blit(txt,(50,y))
            y += 40

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                return

        pygame.display.update()

def main():
    username = get_username()

    while True:
        game = Game(screen, username)

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP and game.direction!=(0,1):
                        game.direction=(0,-1)
                    if e.key == pygame.K_DOWN and game.direction!=(0,-1):
                        game.direction=(0,1)
                    if e.key == pygame.K_LEFT and game.direction!=(1,0):
                        game.direction=(-1,0)
                    if e.key == pygame.K_RIGHT and game.direction!=(-1,0):
                        game.direction=(1,0)

            running = game.update()
            game.draw()

            pygame.display.update()
            clock.tick(game.speed)

        save_game(username, game.score, game.level)
        show_leaderboard()

main()