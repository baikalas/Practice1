import pygame, sys, random, json, os
from pygame.locals import *

pygame.init()
pygame.mixer.init()

FPS = 60
clock = pygame.time.Clock()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# COLORS
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
GOLD=(255,215,0)
SILVER=(192,192,192)
BRONZE=(205,127,50)

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 40)

# ---------- LOAD IMAGES ----------
background = pygame.image.load("AnimatedStreet.png").convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

# ---------- LOAD SOUNDS ----------
crash_sound = pygame.mixer.Sound("crash.wav")
coin_sound = pygame.mixer.Sound("collectcoin.mp3")

crash_sound.set_volume(0.7)
coin_sound.set_volume(0.5)

pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.4)

# ---------- LEADERBOARD ----------
FILE = "leaderboard.json"

def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE,"r") as f:
        return json.load(f)

def save(name, score, dist):
    data = load()
    data.append({"name":name,"score":score,"distance":int(dist)})
    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)

# ---------- UTILS ----------
def draw_center(text, y, size="small", color=BLACK):
    f = font_small if size=="small" else font_big
    img = f.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    screen.blit(img, rect)

def draw_health_bar(x,y,w,h,health,maxh):
    ratio = health/maxh
    pygame.draw.rect(screen, RED,(x,y,w,h))
    pygame.draw.rect(screen, GREEN,(x,y,w*ratio,h))

def safe_x(existing):
    for _ in range(10):
        x=random.randint(40,360)
        if all(abs(s.rect.centerx-x)>60 for s in existing):
            return x
    return random.randint(40,360)

# ---------- CLASSES ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Player.png").convert_alpha()
        self.rect=self.image.get_rect(center=(200,500))
        self.health=100
        self.max_health=100
        self.shield=False

    def move(self):
        k=pygame.key.get_pressed()
        if k[K_LEFT] and self.rect.left>0:
            self.rect.x-=5
        if k[K_RIGHT] and self.rect.right<WIDTH:
            self.rect.x+=5

class Enemy(pygame.sprite.Sprite):
    def __init__(self,speed,existing):
        super().__init__()
        self.image=pygame.image.load("Enemy.png").convert_alpha()
        self.rect=self.image.get_rect(center=(safe_x(existing),0))
        self.speed=speed
    def update(self):
        self.rect.y+=self.speed
        if self.rect.top>HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self,speed,existing):
        super().__init__()
        self.image=pygame.image.load("coin.png").convert_alpha()
        self.rect=self.image.get_rect(center=(safe_x(existing),0))
        self.speed=speed
    def update(self):
        self.rect.y+=self.speed
        if self.rect.top>HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self,kind,speed,existing):
        super().__init__()
        self.kind=kind
        self.speed=speed

        if kind=="Nitro":
            self.image=pygame.image.load("nitro.png").convert_alpha()
        elif kind=="Shield":
            self.image=pygame.image.load("shield.png").convert_alpha()
        else:
            self.image=pygame.image.load("repair.png").convert_alpha()

        self.image=pygame.transform.scale(self.image,(40,40))
        self.rect=self.image.get_rect(center=(safe_x(existing),0))

    def update(self):
        self.rect.y+=self.speed
        if self.rect.top>HEIGHT:
            self.kill()

# ---------- GAME ----------
def start():
    global player,enemies,coins,powers
    global SPEED,SCORE,DIST,state
    global last_e,last_c,last_p
    global username,bg_y

    player=Player()
    enemies=pygame.sprite.Group()
    coins=pygame.sprite.Group()
    powers=pygame.sprite.Group()

    SPEED=5
    SCORE=0
    DIST=0

    last_e=last_c=last_p=0
    username=""
    bg_y = 0

    pygame.mixer.music.play(-1)

    state="game"

# ---------- MAIN ----------
state="menu"
username=""
bg_y = 0

while True:

    for e in pygame.event.get():
        if e.type==QUIT:
            pygame.quit();sys.exit()

        if e.type==MOUSEBUTTONDOWN:
            if state=="menu":
                start()
            elif state=="leaderboard":
                state="menu"

        if state=="enter_name" and e.type==KEYDOWN:
            if e.key==K_RETURN and username.strip():
                save(username,SCORE,DIST)
                state="leaderboard"
            elif e.key==K_BACKSPACE:
                username=username[:-1]
            else:
                if len(username)<12:
                    username+=e.unicode

    # MENU
    if state=="menu":
        screen.fill(WHITE)
        draw_center("RACER",150,"big")
        draw_center("Click to Play",300)

    # GAME
    elif state=="game":

        bg_y += SPEED
        if bg_y >= HEIGHT:
            bg_y = 0

        screen.blit(background,(0,bg_y))
        screen.blit(background,(0,bg_y-HEIGHT))

        player.move()
        now=pygame.time.get_ticks()

        player.health-=0.02

        if now-last_e>1000:
            enemies.add(Enemy(SPEED,enemies))
            last_e=now

        if now-last_c>1200:
            coins.add(Coin(SPEED,enemies))
            last_c=now

        if now-last_p>4000:
            powers.add(PowerUp(random.choice(["Nitro","Shield","Repair"]),SPEED,enemies))
            last_p=now

        enemies.update(); coins.update(); powers.update()

        screen.blit(player.image,player.rect)
        for g in [enemies,coins,powers]:
            for s in g: screen.blit(s.image,s.rect)

        # collisions
        hits=pygame.sprite.spritecollide(player,enemies,True)
        if hits:
            if player.shield:
                player.shield=False
            else:
                crash_sound.play()
                player.health-=25

        for c in pygame.sprite.spritecollide(player,coins,True):
            coin_sound.play()
            SCORE+=5

        hit=pygame.sprite.spritecollideany(player,powers)
        if hit:
            if hit.kind=="Shield":
                player.shield=True
            elif hit.kind=="Nitro":
                SPEED+=3
            elif hit.kind=="Repair":
                player.health=min(player.max_health,player.health+30)
            hit.kill()

        if player.health<=0:
            crash_sound.play()
            pygame.mixer.music.stop()
            state="enter_name"

        DIST+=0.1

        draw_center(f"Score: {SCORE}",30)
        draw_health_bar(100,60,200,15,player.health,player.max_health)

    # NAME INPUT
    elif state=="enter_name":
        screen.fill(WHITE)
        draw_center("GAME OVER",150,"big")
        draw_center("Enter Name:",230)

        pygame.draw.rect(screen,BLACK,(100,260,200,40),2)
        draw_center(username,280)

        draw_center("Press ENTER",340)

    # LEADERBOARD
    elif state=="leaderboard":
        screen.fill(WHITE)
        data=sorted(load(),key=lambda x:x['score'],reverse=True)[:10]

        draw_center("TOP 10",60,"big")

        y=120
        for i,d in enumerate(data):
            color=BLACK
            if i==0: color=GOLD
            elif i==1: color=SILVER
            elif i==2: color=BRONZE

            draw_center(f"{i+1}. {d['name']}  {d['score']}",y,color=color)
            y+=35

        draw_center("Click to Menu",540)

    pygame.display.update()
    clock.tick(FPS)