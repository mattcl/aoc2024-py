"""01: Historian Hysteria"""

import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.left = []
        self.right = []
        self.counts = {}

        for line in input.strip().split("\n"):
            parts = line.split(" ", maxsplit=1)
            lv = int(parts[0].strip())
            rv = int(parts[1].strip())

            if rv in self.counts:
                self.counts[rv] += 1
            else:
                self.counts[rv] = 1

            self.left.append(lv)
            self.right.append(rv)

        self.left.sort()
        self.right.sort()

    def part_one(self) -> int:
        return sum(abs(lv - rv) for lv, rv in zip(self.left, self.right))

    def part_two(self) -> int:
        return sum(v * self.counts.get(v, 0) for v in self.left)
