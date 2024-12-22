"""22: monkey market"""
from collections import defaultdict
from functools import reduce
from multiprocessing import Pool

import aoc.util


# N % 16,777,216 is equal to N & MOD_MASK;
MOD_MASK = (1 << 24) - 1
SEQ_MASK = (1 << 20) - 1
DESIRED_CHUNKS = 4
UNSEEN = 1 << 22


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        initial_vals = list(map(int, input.strip().split("\n")))

        groups = list(make_groups(initial_vals, 8))

        with Pool() as pool:
            num_total, best, totals = reduce(converge, pool.imap_unordered(compute, groups))

            self.p1 = num_total
            self.p2 = best

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


def default():
    return 0


def pool_init():
    global totals

    totals = defaultdict(default)


def compute(values):
    totals = defaultdict(default)

    num_total = 0
    best = 0

    for i, n in enumerate(values):
        seen = set()
        cur = n
        key = 0
        prev = cur % 10

        for j in range(2000):
            cur = next_number(cur)
            cur_digit = cur % 10
            delta = cur_digit - prev
            prev = cur_digit
            key = ((key << 5) & SEQ_MASK) | (delta + 10)

            if j > 2 and key not in seen:
                seen.add(key)
                totals[key] += cur_digit
                best = max(best, totals[key])

        num_total += cur

    return [num_total, best, totals]


def next_number(input: int) -> int:
    a = input ^ (input << 6) & MOD_MASK
    a = a ^ (a >> 5)
    return a ^ ((a << 11) & MOD_MASK)


def make_groups(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def converge(acc, args):
    acc[0] += args[0]
    acc[1] = max(acc[1], args[1])

    for k, v in args[2].items():
        acc[2][k] += v
        acc[1] = max(acc[1], acc[2][k])

    return acc
