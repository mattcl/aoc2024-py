"""07: bridge repair"""
import math
from multiprocessing import Pool

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.p1 = 0
        self.p2 = 0

        args = map(lambda parts: (int(parts[0]), list(map(int, parts[1].split(' ')))), map(lambda line: line.split(": "), input.strip().split("\n")))

        with Pool() as pool:
            results = pool.map(combined_dfs, args)
            for a, b in results:
                self.p1 += a
                self.p2 += b

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


# too slow doing this in python
# def combined_dfs(args) -> (int, int):
#     target, values = args
#     num_values = len(values)
#     valid = [False, False]
#     _combined_dfs(target, 1, num_values, values, values[0], False, valid)

#     if valid[0]:
#         return (target, target)

#     if valid[1]:
#         return (0, target)

#     return (0, 0)


def combined_dfs(args) -> (int, int):
    target, values = args
    num_values = len(values)

    if _p1_dfs(target, 1, num_values, values, values[0]):
        return (target, target)

    if _p2_dfs(target, 1, num_values, values, values[0]):
        return (0, target)

    return (0, 0)


def _p1_dfs(target, idx, num_values, values, head) -> bool:
    if idx == num_values:
        return target == head

    if head > target:
        return False

    v = values[idx]
    next_idx = idx + 1

    return _p1_dfs(target, next_idx, num_values, values, head * v) or _p1_dfs(target, next_idx, num_values, values, head + v)


def _p2_dfs(target, idx, num_values, values, head) -> bool:
    if idx == num_values:
        return head == target

    if head > target:
        return

    v = values[idx]
    next_idx = idx + 1

    width = int(math.log10(v)) + 1
    return _p2_dfs(target, next_idx, num_values, values, head * pow(10, width) + v) or _p2_dfs(target, next_idx, num_values, values, head * v) or _p2_dfs(target, next_idx, num_values, values, head + v)


# this is slower in python
def _combined_dfs(target, idx, num_values, values, head, used_concat, valid):
    if idx == num_values:
        if head == target:
            valid[1] = True
            if not used_concat:
                valid[0] = True
        return

    if head > target:
        return

    v = values[idx]
    next_idx = idx + 1

    if not valid[1]:
        width = int(math.log10(v)) + 1
        _combined_dfs(target, next_idx, num_values, values, head * pow(10, width) + v, True, valid)

    _combined_dfs(target, next_idx, num_values, values, head * v, used_concat, valid)

    if valid[0]:
        return

    _combined_dfs(target, next_idx, num_values, values, head + v, used_concat, valid)


