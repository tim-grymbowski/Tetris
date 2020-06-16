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

# ----------------------------------------------- take care of this
def clearAnyLines(grid):
    """
    (Used if not isSelected)
    Can be used as score += clearAnyLines(grid) * 10 if clearAnyLines(grid) < 4 else clearAnyLines(grid) * 40

    Is the algorithm below "correct" ?

    y = current_piece.y
    filled_rows = []
    for v in range(4):
        isFilled = True
        for w in range(width):
            if grid[y + v][w] == 0:
                isFilled = False
        if isFilled:
            filled_rows.append(v)
    
    for row in filled_rows:
        grid[row] = [0 for _ in range(width)]

        pg.time.delay(400)
        win.blit((0, 0, 0), rect, 0)
        pg.display.update()
        grid.remove(grid[row])
        grid.insert((some function of filled_rows.index(row), len(filled_rows), maybe height), [0 for _ in range(width)])

    win.blit((0, 0, 0), rect, 0)
    pg.display.update()

    return len(filled_rows)
    """
    pass

def isGameOver(grid):
    for u in range(4):
        for v in range(4):
            if grid[v][u + 3] != 0:
                return True
    return False

def drawGrid(win, c, grid):

    """
    What is still not clear is what to use for rect, respectively.
    """

    for h in len(grid):
        for w in len(h):
            u, v = w - x, h - y
            if u in range(4) and v in range(4):
                # rect == ?
                win.blit(color((c.shape)[rotate(u, v, r)]), rect, 0)
            else:
                # rect == ?
                win.blit(color(grid[h][w]), rect, 0)   

# ----------------------------------------------- still somewhat of a mystery
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
            
            # not sure if this should go here or after calling isGameOver
            clearAnyLines(grid) 

            if isGameOver(grid):
                run = False
                # just for now, we'll find a better way later
                sys.exit()

            if not isSelected:
                current_piece = Tetromino(3, 0, 0)
                isSelected = True

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

