import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

current_color = BLACK

# Tools
TOOL_BRUSH = "brush"
TOOL_RECT  = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"

current_tool = TOOL_BRUSH

drawing = False
start_pos = None

screen.fill(WHITE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYBOARD TOOL SWITCH
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = TOOL_BRUSH
            elif event.key == pygame.K_2:
                current_tool = TOOL_RECT
            elif event.key == pygame.K_3:
                current_tool = TOOL_CIRCLE
            elif event.key == pygame.K_4:
                current_tool = TOOL_ERASER

            # COLOR SELECTION
            elif event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE
            elif event.key == pygame.K_k:
                current_color = BLACK

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            end_pos = event.pos

            if current_tool == TOOL_RECT:
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])

                pygame.draw.rect(screen, current_color, (x, y, w, h))

            elif current_tool == TOOL_CIRCLE:
                radius = int(((start_pos[0] - end_pos[0])**2 +
                              (start_pos[1] - end_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius)

    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if current_tool == TOOL_BRUSH:
            pygame.draw.circle(screen, current_color, mouse_pos, 5)

        elif current_tool == TOOL_ERASER:
            pygame.draw.circle(screen, WHITE, mouse_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()