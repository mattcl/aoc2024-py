"""12: garden groups"""
from collections import deque

import aoc.util

NORTH = 1
NE = 2
EAST = 4
SE = 8
SOUTH = 16
SW = 32
WEST = 64
NW = 128

CARDINAL = NORTH | EAST | WEST | SOUTH

# Corner checking BS
UL = NORTH | WEST | NW
UR = NORTH | EAST | NE
LL = SOUTH | WEST | SW
LR = SOUTH | EAST | SE

ULI = 0
ULO = NORTH | WEST
ULN = NW

URI = 0
URO = NORTH | EAST
URN = NE

LLI = 0
LLO = SOUTH | WEST
LLN = SW

LRI = 0
LRO = SOUTH | EAST
LRN = SE

DIRS = [
    (-1, 0, NORTH),
    (-1, 1, NE),
    (0, 1, EAST),
    (1, 1, SE),
    (1, 0, SOUTH),
    (1, -1, SW),
    (0, -1, WEST),
    (-1, -1, NW),
]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        grid = list(input.strip().split("\n"))
        height = len(grid)

        seen_grid = [0] * height
        cur = deque([])

        self.p1 = 0
        self.p2 = 0

        for gr in range(height):
            for gc in range(height):
                if not contains(seen_grid, gr, gc):
                    corners = 0
                    perimeter = 0
                    area = 0
                    v = grid[gr][gc]
                    cur.append((gr, gc))
                    while cur:
                        r, c = cur.popleft()

                        if contains(seen_grid, r, c):
                            continue

                        insert(seen_grid, r, c)

                        area += 1

                        num_edges = 4
                        dir_map = 0

                        for dr, dc, dir in DIRS:
                            nr = r + dr
                            nc = c + dc

                            if nr < 0 or nr >= height or nc < 0 or nc >= height:
                                continue

                            nv = grid[nr][nc]

                            if nv == v:
                                dir_map |= dir

                                if dir & CARDINAL != 0:
                                    num_edges -= 1
                                    if not contains(seen_grid, nr, nc):
                                        cur.append((nr, nc))

                        if dir_map == 0:
                            corners += 4
                        else:
                            ul = dir_map & UL
                            if ul == ULI or ul == ULO or ul == ULN:
                                corners += 1

                            ur = dir_map & UR
                            if ur == URI or ur == URO or ur == URN:
                                corners += 1

                            ll = dir_map & LL
                            if ll == LLI or ll == LLO or ll == LLN:
                                corners += 1

                            lr = dir_map & LR
                            if lr == LRI or lr == LRO or lr == LRN:
                                corners += 1

                        perimeter += num_edges

                    self.p1 += perimeter * area

                    # corners is equal to sides
                    self.p2 += corners * area

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


def contains(seen_grid, r, c) -> bool:
    return seen_grid[r] & 1 << c != 0


def insert(seen_grid, r, c):
    seen_grid[r] |= 1 << c
