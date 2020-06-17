import pygame as pg
import random
import sys
import os

# i think this works the other way around too
# for loading music from same folder later
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

s_width = 800
s_height = 800

pg.init()
pg.display.set_caption("Tetris")
win = pg.display.set_mode((s_width, s_height))

width = 10
height = 20
block_size = 30

I = "0010001000100010"
J = "0000022002000200"
L = "0000033000300030"
O = "0000044004400000"
S = "0500055000500000"
T = "0060066000600000"
Z = "0070077007000000" 

shapes = [I, J, L, O, S, T, Z]
grid = [[0 for _ in range(width)] for _ in range(height)]

class Tetromino:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.shape = random.choice(shapes)

def colors(k):
    if k == 0:
        return (0, 0, 0)
    elif k == 1:
        return (0, 255, 255)
    elif k == 2:
        return (0, 0, 255)
    elif k == 3:
        return (255, 128, 0)
    elif k == 4:
        return (255, 255, 0)
    elif k == 5:
        return (0, 255, 0)
    elif k == 6:
        return (255, 0, 255)
    return (255, 0, 0)

def rotate(u, v, r):
    if r % 4 == 0:
        return u + 4 * v
    elif r % 4 == 1:
        return 12 - 4 * u + v
    elif r % 4 == 2:
        return 15 - u - 4 * v
    return 3 + 4 * u - v

def valid(c, x, y, r):
    for u in range(4):
        for v in range(4):
            p = rotate(u, v, r)
            g = x + u, v + y
            if (c.shape[p]) != 0:
                if g[0] not in range(width) or g[1] >= height:
                    return False
                elif grid[g[1]][g[0]] != 0:
                    return False
    return True

# (Used if not isSelected)
# Can be used as score += clearAnyLines(grid) * 10 if clearAnyLines(grid) < 4 else clearAnyLines(grid) * 40
def clearAnyLines(grid, current_piece):
    # either display new score (or keep old score) at the end or after or outside the conditional
    y = current_piece.y
    # play around with these values
    m, n = 6, 6
    filled_rows = []
    for v in range(4):
        isFilled = True
        for w in range(width):
            if grid[y + v][w] == 0:
                isFilled = False
        if isFilled:
            filled_rows.append(y + v)

    for row in filled_rows:
        grid[row] = [0 for _ in range(width)]

        pg.time.delay(400)
        pg.draw.rect(win, (0, 0, 0), (m, n + grid.index(row) * block_size, m + width * block_size - 1, n + (grid.index(row) + 1) * block_size - 1), 0)
        pg.display.update()
        grid.remove(grid[filled_rows[len(filled_rows) - 1 - filled_rows.index(row)]])
        grid.insert(0, [0 for _ in range(width)])

    pg.draw.rect(win, (0, 0, 0), (m, n, m + width * block_size - 1, n + 4 * block_size - 1), 0)
    pg.display.update()

    return len(filled_rows)

def isGameOver(grid):
    for u in range(4):
        for v in range(4):
            if grid[v][u + 3] != 0:
                return True
    return False

def drawGrid(win, c, grid):
    # either call pg.display.update at the end or after
    x, y, r = c.x, c.y, c.r
    for h in range(height):
        for w in range(width):
            u, v = w - x, h - y
            if u in range(4) and v in range(4):
                pg.draw.rect(win, colors((c.shape)[rotate(u, v, r)]), (w * block_size, h * block_size, (w + 1) * block_size - 1, (h + 1) * block_size - 1), 0)
            else:
                pg.draw.rect(win, colors(grid[h][w]), (w * block_size, h * block_size, (w + 1) * block_size - 1, (h + 1) * block_size - 1), 0)   

# ----------------------------------------------- still somewhat of a mystery

# maybe just use size_x, size_y for dimensions (for rect)?
def main(win):
    run = True
    clock = pg.time.Clock()
    time_tick = 50
    time_elapsed = 0
    isSelected = True
    current_piece = Tetromino(3, 0, 0)

    # in which places do we use pg.display.update() ?
    while run:
        time_elapsed += clock.get_rawtime()
        clock.tick()

        if time_elapsed == time_tick:
            if valid(current_piece, current_piece.x, current_piece.y + 1, current_piece.r):
                current_piece.y += 1  
            else:
                isSelected = False
                for u in range(4):
                    for v in range(4):
                        # THERE USED TO BE AN INDEXERROR HERE
                        y = current_piece.y; x = current_piece.x; r = current_piece.r
                        grid[y + v][x + u] = (current_piece.shape)[rotate(u, v, r)] if (current_piece.shape)[rotate(u, v, r)] else grid[y + v][x + u]
            
            clearAnyLines(grid, current_piece) 

            if not isSelected:
                current_piece = Tetromino(3, 0, 0)
                isSelected = True

            if isGameOver(grid):
                run = False
                # just for now, we'll find a better way later
                sys.exit()

            drawGrid(win, current_piece, grid)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                sys.exit()

            # this actually keeps us stuck if we keep holding a key down
            # therefore we need a one-time register for each click
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1 if valid(current_piece, current_piece.x - 1, current_piece.y, current_piece.r) else 0
                if event.key == pg.K_RIGHT:
                    current_piece.x += 1 if valid(current_piece, current_piece.x + 1, current_piece.y, current_piece.r) else 0
                if event.key == pg.K_UP:
                    current_piece.r += 1 if valid(current_piece, current_piece.x, current_piece.y, current_piece.r + 1) else 0
                if event.key == pg.K_DOWN:
                    current_piece.y += 1 if valid(current_piece, current_piece.x, current_piece.y + 1, current_piece.r) else 0
            drawGrid(win, current_piece, grid)

# fix buttons and add menu later
if __name__ == "__main__":
    main(win)

