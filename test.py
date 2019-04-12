import pygame
import pygame.gfxdraw
import math
import time
from random import randint


class node:
    def __init__(self, x, y, sz):
        self.x = x
        self.y = y
        self.sz = sz
        self.col = 7


class block:
    def __init__(self, y, x, sz, occ, orient, col):
        self.x = x  # coordinates of upper left corner of rotation area
        self.y = y
        self.sz = sz  # size of rotation grid
        self.occ = occ  # grid squares occupied by block
        self.orient = orient  # orientation of block
        self.col = col


width = 10
height = 20

grid = [[None for x in range(width)] for x in range(height)]

colours = [(0, 255, 255),   # 0 - cyan (long boi)
           (0, 0, 255),     # 1 - blue (J piece)
           (255, 165, 0),   # 2 - orange (L piece)
           (255, 255, 0),   # 3 - yellow (square)
           (0, 128, 0),     # 4 - green (S piece)
           (255, 0, 0),     # 5 - red (Z piece)
           (128, 0, 128),   # 6 - purple (T piece)
           (0, 0, 0),       # 7 - black (empty)
           (255, 255, 255)] # 8 - white (clear)

ghosts = [(0, 128, 128),    # 0 - cyan (long boi)
          (0, 0, 128),      # 1 - blue (J piece)
          (128, 82, 0),    # 2 - orange (L piece)
          (128, 128, 0),    # 3 - yellow (square)
          (0, 64, 0),      # 4 - green (S piece)
          (128, 0, 0),      # 5 - red (Z piece)
          (64, 0, 64)]    # 6 - purple (T piece)

# format: rotates in x by x grid, with [a,b], [c,d] ... blocks coloured
types = [[4, [1, 0], [1, 1], [1, 2], [1, 3]],  # long boi (spawns vertical right)
         [3, [0, 0], [1, 0], [1, 1], [1, 2]],  # J piece (spawns pointy down)
         [3, [1, 0], [1, 1], [1, 2], [0, 2]],  # L piece (spawns pointy down)
         [2, [0, 0], [0, 1], [1, 0], [1, 1]],  # square piece
         [3, [1, 0], [1, 1], [0, 1], [0, 2]],  # S piece (spawns vertical)
         [3, [0, 0], [0, 1], [1, 1], [1, 2]],  # Z piece (spawns vertical)
         [3, [0, 1], [1, 0], [1, 1], [1, 2]]]  # T piece (spawns upside down)

for i in range(height):
    for j in range(width):
        grid[i][j] = node(j * 30 + 10, i * 30 + 10, 29)


def paintGrid(screen):
    screen.fill((128, 128, 128), rect=[0, 0, 321, 621])
    for i in range(height):
        for j in range(width):
            cur = grid[i][j]
            screen.fill(colours[cur.col], [cur.x, cur.y, cur.sz, cur.sz])


def ghostBlock(screen, cur):
    arr = []
    arr2 = []
    for i in cur.occ:
        y, x = cur.y + i[0], cur.x + i[1]
        arr.append([y, x])
        arr2.append([y, x])
    canFall = 1
    mod = 0
    while canFall:
        for [y, x] in arr:
            if y == 19 or (grid[y + 1][x].col != 7 and [y + 1, x] not in arr):
                canFall = 0
        if canFall:
            mod += 1
            for i in arr:
                i[0] += 1
    for i in arr:
        if i in arr2:
            continue
        temp = grid[i[0]][i[1]]
        screen.fill(ghosts[cur.col], [temp.x, temp.y, temp.sz, temp.sz])


def shift(val, cur):
    for i in cur.occ:
        y, x = cur.y + i[0], cur.x + i[1]
        x += val
        if x < 0 or x >= 10 or (grid[y][x].col != 7 and [i[0], i[1] + val] not in cur.occ):
            return cur

    for i in cur.occ:
        y, x = cur.y + i[0], cur.x + i[1]
        grid[y][x].col = 7

    cur.x += val

    for i in cur.occ:
        y, x = cur.y + i[0], cur.x + i[1]
        grid[y][x].col = cur.col

    return cur


def rotate(val, cur):
    mod = [0, 0]  # for wall-kicks (TO BE IMPLEMENTED)
    occ2 = []

    for i in cur.occ:
        if val == 1:
            occ2.append([cur.sz - i[1] - 1, i[0]])
        else:
            occ2.append([i[1], cur.sz - i[0] - 1])

    for i in occ2:
        y, x = cur.y + i[0], cur.x + i[1]
        if y < 0 or x < 0 or x >= 10 or (grid[y][x].col != 7 and [i[0], i[1]] not in cur.occ):
            return cur

    for i in cur.occ:
        y, x = cur.y + i[0], cur.x + i[1]
        grid[y][x].col = 7

    for i in occ2:
        y, x = cur.y + i[0], cur.x + i[1]
        grid[y][x].col = cur.col

    cur.occ = occ2
    return cur


def clearLines(screen):
    lines = 0
    for i in range(19, -1, -1):     #get lines that are cleared
        f = 1
        for j in range(10):
            if grid[i][j].col == 7:
                f = 0
        if f:
            lines += 1
            for j in range(10):
                grid[i][j].col = 8
    if not lines:
        return 0

    paintGrid(screen)
    pygame.display.flip()
    time.sleep(0.2)
    lines = 0
    for i in range(19, -1, -1):
        if grid[i][0].col == 8:
            lines += 1
            for j in range(10):
                grid[i][j].col = 7
        else:
            for j in range(10):
                grid[i+lines][j].col = grid[i][j].col
                if lines:
                    grid[i][j].col = 7
    return lines


def hardDrop(cur):
    canFall = 1
    while canFall:
        for i in cur.occ:
            y, x = cur.y + i[0], cur.x + i[1]
            grid[y][x].col = cur.col
            if y == 19 or (grid[y + 1][x].col != 7 and [i[0] + 1, i[1]] not in cur.occ):
                canFall = 0
        if canFall:
            for i in cur.occ:
                y, x = cur.y + i[0], cur.x + i[1]
                grid[y][x].col = 7
            cur.y += 1
            for i in cur.occ:
                y, x = cur.y + i[0], cur.x + i[1]
                grid[y][x].col = cur.col


def genBlock(last):
    num = randint(1, sum(last))
    tot = 0
    for i in range(7):
        tot += last[i]
        if num <= tot:
            return i


def runGame(screen):
    paintGrid(screen)
    clock = pygame.time.Clock()
    score = 0
    alive = 1
    locked = 1
    cnt = 0
    interval = 20
    buffer = 0      # buffer for rotation
    buffer2 = 0     # buffer for hard drop
    level = 0

    last = [1 for x in range(7)]    # how many rounds ago last spawned
    add = [1 for x in range(7)]

    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if locked:  # if last block dropped has been locked into place
            lines = clearLines(screen)
            curType = genBlock(last)    # generate block type

            for i in range(7):          # modify block probabilities
                if i == curType:
                    last[i] = 1
                    add[i] = 1
                else:
                    last[i] += add[i]
                    add[i] += 1

            cur = block(0, 5 - types[curType][0] // 2, types[curType][0], types[curType][1:], 0, curType)
            for i in cur.occ:
                y, x = cur.y + i[0], cur.x + i[1]
                grid[y][x].col = cur.col
            locked = 0
            cnt = 0
            paintGrid(screen)

        keys = pygame.key.get_pressed()
        mod = [0, 0]  # position modifications (shift, rotation)
        if keys[pygame.K_SPACE] and buffer <= 0:
            hardDrop(cur)
            paintGrid(screen)
            locked = 1
            buffer = 8
            continue
        if keys[pygame.K_LEFT]:
            mod[0] -= 1
        if keys[pygame.K_RIGHT]:
            mod[0] += 1
        if keys[pygame.K_UP] and buffer2 <= 0:
            mod[1] -= 1
            buffer2 = 4
        if keys[pygame.K_DOWN]:
            cnt += interval/2
        if mod[0]:
            cur = shift(mod[0], cur)
        if mod[1]:
            cur = rotate(mod[1], cur)

        cnt += 1
        buffer -= 1
        buffer2 -= 1
        if cnt >= interval:
            for i in cur.occ:
                y, x = cur.y + i[0], cur.x + i[1]
                grid[y][x].col = cur.col
                if y == 19 or (grid[y + 1][x].col != 7 and [i[0] + 1, i[1]] not in cur.occ):
                    locked = 1
            if not locked:
                for i in cur.occ:
                    y, x = cur.y + i[0], cur.x + i[1]
                    grid[y][x].col = 7
                cur.y += 1
                for i in cur.occ:
                    y, x = cur.y + i[0], cur.x + i[1]
                    grid[y][x].col = cur.col
            cnt = 0

        level += 1

        if level >= 1000 and interval > 5:
            level = 0
            interval -= 2

        paintGrid(screen)
        ghostBlock(screen, cur)
        pygame.display.flip()
        clock.tick(25)


def main():
    pygame.init()
    screen = pygame.display.set_mode((521, 621))
    pygame.display.set_caption("Tetris!")
    clock = pygame.time.Clock()
    pygame.display.flip()
    running = 1
    paintGrid(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        '''
        bx,by = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if bx >= 304 and bx <= 509:
            if by >= 376 and by <= 431:
                screen.blit(play,(0,0))
                if 1 in click:
                    runGame(screen)
                    screen.blit(title,(0,0))
            elif by >= 446 and by <= 501:
                screen.blit(settings,(0,0))
            elif by >= 518 and by <= 573:
                screen.blit(controls,(0,0))
            else:
                screen.blit(title,(0,0))
        else:
            screen.blit(title,(0,0))
        '''
        runGame(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()

'''

Current bugs:


To do list:
- Randomized spawns
- Wall kicks
- Points system
- Main menu
- "Next block"
- "Hold block"
- Make blocks spawn above grid
- Loss condition

Long term:
- Two-player?


'''