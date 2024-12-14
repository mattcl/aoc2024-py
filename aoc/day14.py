"""14: restroom redoubt"""
import math

import aoc.util

WIDTH = 101
HEIGHT = 103

MID_X = WIDTH // 2
MID_Y = HEIGHT // 2


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        self.guards = []
        for line in input.replace("v=", "").replace("p=", "").replace(",", " ").strip().split("\n"):
            parts = list(map(int, line.split(" ")))

            self.guards.append((parts[0], parts[1], parts[2], parts[3]))

    def part_one(self) -> int:
        counts = [0, 0, 0, 0]

        for guard in self.guards:
            pos = bounded(guard, 100)
            q = quadrant(pos)
            if q != -1:
                counts[q] += 1

        return math.prod(counts)

    def part_two(self) -> int:
        seen = [0] * HEIGHT
        for i in range(3000, 10000):
            for guard in self.guards:
                pos = bounded(guard, i)
                mask = 1 << pos[0]

                if seen[pos[1]] & mask != 0:
                    seen = [0] * HEIGHT
                    break

                seen[pos[1]] |= mask

            if seen[MID_Y] > 0:
                return i

        return -1


def bounded(guard, seconds) -> (int, int):
    x, y, dx, dy = guard

    # % is fine here because python % is actually rem_euclid
    return (
        (x + dx * seconds) % WIDTH,
        (y + dy * seconds) % HEIGHT
    )


def quadrant(point) -> int:
    x, y = point
    if x == MID_X or y == MID_Y:
        return -1

    upper = y < MID_Y
    left = x < MID_X

    if upper and left:
        return 0

    if upper and not left:
        return 1

    if not upper and not left:
        return 2

    return 3
