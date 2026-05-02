import sys
from datetime import datetime

import pygame

from tools import (
    ALL_TOOLS, BRUSH_SIZES, ERASER_MULT,
    TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_CIRCLE,
    TOOL_ERASER, TOOL_FILL, TOOL_TEXT,
    flood_fill,
)

pygame.init()

WIDTH          = 900
TOOLBAR_H      = 58
CANVAS_H       = 592
HEIGHT         = TOOLBAR_H + CANVAS_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint — TSIS2")
clock  = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, CANVAS_H))
canvas.fill((255, 255, 255))

BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (220, 30,  30)
GREEN   = (30,  160, 30)
BLUE    = (30,  30,  220)
YELLOW  = (240, 210, 0)
ORANGE  = (240, 130, 0)
PURPLE  = (140, 0,   200)
CYAN    = (0,   200, 200)
PINK    = (240, 80,  160)

PALETTE = [BLACK, WHITE, RED, GREEN, BLUE,
           YELLOW, ORANGE, PURPLE, CYAN, PINK]

current_color     = BLACK
current_tool      = TOOL_PENCIL
brush_size_index  = 1
brush_size        = BRUSH_SIZES[brush_size_index]

drawing   = False
start_pos = None
last_pos  = None

text_active = False
text_pos    = None
text_input  = ""

ui_font   = pygame.font.SysFont("segoeui",  13)
text_font = pygame.font.SysFont("arial",    24)

BTN_Y  = 7
BTN_H  = 44
GAP    = 3

TOOL_BTN_W = 56
TOOL_BTN_X = 5

SZ_BTN_W = 38
SZ_BTN_X = TOOL_BTN_X + len(ALL_TOOLS) * (TOOL_BTN_W + GAP) + 8

COL_W  = 26
COL_H  = 36
COL_X  = SZ_BTN_X + len(BRUSH_SIZES) * (SZ_BTN_W + GAP) + 8
COL_Y  = BTN_Y + (BTN_H - COL_H) // 2

TOOL_LABELS = {
    TOOL_PENCIL: ("Pencil", "P"),
    TOOL_LINE:   ("Line",   "L"),
    TOOL_RECT:   ("Rect",   "R"),
    TOOL_CIRCLE: ("Circle", "C"),
    TOOL_ERASER: ("Eraser", "E"),
    TOOL_FILL:   ("Fill",   "F"),
    TOOL_TEXT:   ("Text",   "T"),
}

def to_canvas(screen_pos):
    
    return (screen_pos[0], screen_pos[1] - TOOLBAR_H)

def to_screen(canvas_pos):
    
    return (canvas_pos[0], canvas_pos[1] + TOOLBAR_H)

def tool_rect(index):
    x = TOOL_BTN_X + index * (TOOL_BTN_W + GAP)
    return pygame.Rect(x, BTN_Y, TOOL_BTN_W, BTN_H)

def size_rect(index):
    x = SZ_BTN_X + index * (SZ_BTN_W + GAP)
    return pygame.Rect(x, BTN_Y, SZ_BTN_W, BTN_H)

def color_rect(index):
    x = COL_X + index * (COL_W + 3)
    return pygame.Rect(x, COL_Y, COL_W, COL_H)

def draw_toolbar():
    
    pygame.draw.rect(screen, (210, 215, 222), (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, (160, 165, 172), (0, TOOLBAR_H - 1), (WIDTH, TOOLBAR_H - 1), 2)

    for i, tool_id in enumerate(ALL_TOOLS):
        rect    = tool_rect(i)
        active  = (tool_id == current_tool)
        bg      = (140, 180, 255) if active else (230, 233, 238)
        border  = (60, 100, 200)  if active else (160, 165, 172)
        label, key = TOOL_LABELS[tool_id]

        pygame.draw.rect(screen, bg,     rect, border_radius=5)
        pygame.draw.rect(screen, border, rect, 2 if active else 1, border_radius=5)

        t1 = ui_font.render(label, True, BLACK)
        t2 = ui_font.render(f"[{key}]", True, (80, 80, 80))
        screen.blit(t1, t1.get_rect(centerx=rect.centerx, top=rect.top + 6))
        screen.blit(t2, t2.get_rect(centerx=rect.centerx, top=rect.top + 24))

    for i, sz in enumerate(BRUSH_SIZES):
        rect   = size_rect(i)
        active = (i == brush_size_index)
        bg     = (140, 180, 255) if active else (230, 233, 238)
        border = (60, 100, 200)  if active else (160, 165, 172)

        pygame.draw.rect(screen, bg,     rect, border_radius=5)
        pygame.draw.rect(screen, border, rect, 2 if active else 1, border_radius=5)

        dot_r = min(sz, 10)
        pygame.draw.circle(screen, BLACK, (rect.centerx, rect.top + 20), dot_r)
        num = ui_font.render(str(i + 1), True, BLACK)
        screen.blit(num, num.get_rect(centerx=rect.centerx, top=rect.bottom - 18))

    for i, col in enumerate(PALETTE):
        rect = color_rect(i)
        pygame.draw.rect(screen, col, rect, border_radius=3)
        border_col = (255, 200, 0) if col == current_color else (120, 120, 120)
        border_w   = 3              if col == current_color else 1
        pygame.draw.rect(screen, border_col, rect, border_w, border_radius=3)

    hint = ui_font.render("Ctrl+S = save", True, (90, 90, 90))
    screen.blit(hint, (WIDTH - hint.get_width() - 6, TOOLBAR_H - 18))

def draw_preview():
    
    if not drawing or start_pos is None:
        return
    mp       = to_canvas(pygame.mouse.get_pos())
    ss       = to_screen(start_pos)
    ms       = to_screen(mp)
    col      = current_color
    sz       = brush_size

    if current_tool == TOOL_LINE:
        pygame.draw.line(screen, col, ss, ms, sz)

    elif current_tool == TOOL_RECT:
        x = min(ss[0], ms[0])
        y = min(ss[1], ms[1])
        w = abs(ss[0] - ms[0])
        h = abs(ss[1] - ms[1])
        if w > 0 and h > 0:
            pygame.draw.rect(screen, col, (x, y, w, h), sz)

    elif current_tool == TOOL_CIRCLE:
        dx, dy = start_pos[0] - mp[0], start_pos[1] - mp[1]
        radius = int((dx * dx + dy * dy) ** 0.5)
        if radius > 0:
            pygame.draw.circle(screen, col, ss, radius, sz)

def draw_text_cursor():
    
    if not text_active or text_pos is None:
        return
    preview = text_font.render(text_input + "|", True, current_color)
    screen.blit(preview, to_screen(text_pos))

def commit_shape(end_pos):
    
    sp  = start_pos
    ep  = end_pos
    col = current_color
    sz  = brush_size

    if current_tool == TOOL_LINE:
        pygame.draw.line(canvas, col, sp, ep, sz)

    elif current_tool == TOOL_RECT:
        x = min(sp[0], ep[0])
        y = min(sp[1], ep[1])
        w = abs(sp[0] - ep[0])
        h = abs(sp[1] - ep[1])
        if w > 0 and h > 0:
            pygame.draw.rect(canvas, col, (x, y, w, h), sz)

    elif current_tool == TOOL_CIRCLE:
        dx, dy = sp[0] - ep[0], sp[1] - ep[1]
        radius = int((dx * dx + dy * dy) ** 0.5)
        if radius > 0:
            pygame.draw.circle(canvas, col, sp, radius, sz)

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if text_active:
                if event.key == pygame.K_RETURN:
                    if text_input:
                        surf = text_font.render(text_input, True, current_color)
                        canvas.blit(surf, text_pos)
                    text_input  = ""
                    text_pos    = None
                    text_active = False

                elif event.key == pygame.K_ESCAPE:
                    text_input  = ""
                    text_pos    = None
                    text_active = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                elif event.unicode and event.unicode.isprintable():
                    text_input += event.unicode

            else:
                if   event.key == pygame.K_p: current_tool = TOOL_PENCIL
                elif event.key == pygame.K_l: current_tool = TOOL_LINE
                elif event.key == pygame.K_r: current_tool = TOOL_RECT
                elif event.key == pygame.K_c: current_tool = TOOL_CIRCLE
                elif event.key == pygame.K_e: current_tool = TOOL_ERASER
                elif event.key == pygame.K_f: current_tool = TOOL_FILL
                elif event.key == pygame.K_t: current_tool = TOOL_TEXT

                elif event.key == pygame.K_1:
                    brush_size_index = 0
                    brush_size       = BRUSH_SIZES[0]
                elif event.key == pygame.K_2:
                    brush_size_index = 1
                    brush_size       = BRUSH_SIZES[1]
                elif event.key == pygame.K_3:
                    brush_size_index = 2
                    brush_size       = BRUSH_SIZES[2]

                elif (event.key == pygame.K_s and
                      pygame.key.get_mods() & pygame.KMOD_CTRL):
                    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"canvas_{ts}.png"
                    pygame.image.save(canvas, filename)
                    pygame.display.set_caption(f"Mini Paint — saved {filename}")
                    print(f"[Saved] {filename}")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if my <= TOOLBAR_H:
                for i, tool_id in enumerate(ALL_TOOLS):
                    if tool_rect(i).collidepoint(mx, my):
                        current_tool = tool_id
                        break
                for i in range(len(BRUSH_SIZES)):
                    if size_rect(i).collidepoint(mx, my):
                        brush_size_index = i
                        brush_size       = BRUSH_SIZES[i]
                        break
                for i, col in enumerate(PALETTE):
                    if color_rect(i).collidepoint(mx, my):
                        current_color = col
                        break

            else:
                cpos = to_canvas(event.pos)

                if current_tool == TOOL_FILL:
                    flood_fill(canvas, cpos, current_color)

                elif current_tool == TOOL_TEXT:
                    text_pos    = cpos
                    text_active = True
                    text_input  = ""

                else:
                    drawing   = True
                    start_pos = cpos
                    last_pos  = cpos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                cpos = to_canvas(event.pos)

                if current_tool in (TOOL_LINE, TOOL_RECT, TOOL_CIRCLE):
                    commit_shape(cpos)

                drawing   = False
                start_pos = None
                last_pos  = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                cpos = to_canvas(event.pos)

                if current_tool == TOOL_PENCIL:
                    if last_pos:
                        pygame.draw.line(canvas, current_color,
                                         last_pos, cpos, brush_size)
                    last_pos = cpos

                elif current_tool == TOOL_ERASER:
                    er = brush_size * ERASER_MULT
                    pygame.draw.circle(canvas, WHITE, cpos, er)
                    last_pos = cpos

    screen.fill((200, 200, 200))

    screen.blit(canvas, (0, TOOLBAR_H))

    draw_preview()
    draw_text_cursor()

    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()