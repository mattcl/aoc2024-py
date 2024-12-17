"""17: Chronospatial Computer"""
import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        parts = input.strip().split("\n\n")

        self.a = int(parts[0].replace("Register A: ", "").split("\n")[0])
        self.program = list(map(int, parts[1].replace("Program: ", "").split(",")))

        # these are fixed positions in the program that vary between inputs
        #
        # they must always be in their expectd locations
        # expected = [2, 4, 1, v1, 7, 5, 4, v2, 1, v3, 0, 3, 5, 5, 3, 0];

        self.v1 = self.program[3]
        # v2 = self.program[7]
        self.v3 = self.program[9]

    def part_one(self) -> str:
        out = []

        a = self.a

        while a != 0:
            out.append(str(transpiled(a, self.v1, self.v3)))
            a >>= 3

        return ",".join(out)

    def part_two(self) -> int:
        cur = []
        cur.append(0)

        for wanted in reversed(self.program):
            next = []
            for p in cur:
                for i in range(8):
                    a = (p << 3) + i
                    if transpiled(a, self.v1, self.v3) == wanted:
                        next.append(a)

            cur = next

        cur.sort()

        for c in cur:
            digit = 0
            a = c

            while a > 0 and digit < len(self.program):
                digit += 1
                a >>= 3

            if digit == len(self.program):
                return c

        return 0


def transpiled(a, v1, v3) -> int:
    b = (a & 0b111) ^ v1
    return ((b ^ (a >> b)) ^ v3) & 0b111
