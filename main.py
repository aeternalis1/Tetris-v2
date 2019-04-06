import pygame
import pygame.gfxdraw
import math
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

colours = [(0, 255, 255),  # 0 - cyan (long boi)
           (0, 0, 255),  # 1 - blue (J piece)
           (255, 165, 0),  # 2 - orange (L piece)
           (255, 255, 0),  # 3 - yellow (square)
           (0, 128, 0),  # 4 - green (S piece)
           (255, 0, 0),  # 5 - red (Z piece)
           (128, 0, 128),  # 6 - purple (T piece)
           (0, 0, 0)]  # 7 - black (empty)

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


def runGame(screen):
    paintGrid(screen)
    clock = pygame.time.Clock()
    score = 0
    alive = 1
    locked = 1
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if locked:  # if last block dropped has been locked into place
            curType = randint(0, 6)
            cur = block(0, 5 - types[curType][0] // 2, types[curType][0], types[curType][1:], 0, curType)
            for i in cur.occ:
                y, x = cur.y + i[0], cur.x + i[1]
                grid[y][x].col = cur.col
            locked = 0
            paintGrid(screen)

        keys = pygame.key.get_pressed()
        mod = [0, 0]  # position modifications (shift, rotation)
        if keys[pygame.K_LEFT]:
            mod[0] -= 1
        if keys[pygame.K_RIGHT]:
            mod[0] += 1
        if keys[pygame.K_UP]:
            mod[1] += 1
        if keys[pygame.K_DOWN]:
            mod[1] -= 1
        if mod[0]:
            cur = shift(mod[0], cur)
            paintGrid(screen)
        if mod[1]:
            cur = rotate(mod[1], cur)
            paintGrid(screen)

        pygame.display.flip()
        clock.tick(20)


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
- Need to change direction system


To do list:
- Wall kicks
- Add falling blocks

'''