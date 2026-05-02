from collections import deque

TOOL_PENCIL = "pencil"
TOOL_LINE   = "line"
TOOL_RECT   = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"
TOOL_FILL   = "fill"
TOOL_TEXT   = "text"

ALL_TOOLS = [TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_CIRCLE,
             TOOL_ERASER, TOOL_FILL, TOOL_TEXT]

BRUSH_SIZES  = [2, 5, 10]
ERASER_MULT  = 4

def flood_fill(surface, start_pos, fill_color):
    
    sx, sy = int(start_pos[0]), int(start_pos[1])
    width, height = surface.get_size()

    if not (0 <= sx < width and 0 <= sy < height):
        return

    target = surface.get_at((sx, sy))
    target_rgb = (target.r, target.g, target.b)

    fill_rgb = fill_color[:3] if len(fill_color) > 3 else tuple(fill_color)

    if target_rgb == fill_rgb:
        return

    surface.lock()
    try:
        queue   = deque()
        queue.append((sx, sy))
        visited = set()
        visited.add((sx, sy))

        while queue:
            cx, cy = queue.popleft()

            if not (0 <= cx < width and 0 <= cy < height):
                continue

            pixel = surface.get_at((cx, cy))
            if (pixel.r, pixel.g, pixel.b) != target_rgb:
                continue

            surface.set_at((cx, cy), fill_rgb)

            for nx, ny in ((cx + 1, cy), (cx - 1, cy),
                           (cx, cy + 1), (cx, cy - 1)):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    finally:
        surface.unlock()