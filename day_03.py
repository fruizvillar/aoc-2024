""" Solver for AoC 2024 Day 3"""

import functools
import re
from typing import override

import lib

DAY = int("3")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/3"""

    RE_MUL = re.compile(r"mul\((\d+),(\d+)\)")
    RE_DO = re.compile(r"do\(\)")
    RE_DONT = re.compile(r"don't\(\)")

    @override
    def solve(self) -> None:

        data = self.read()

        result_1 = result_2 = 0

        does = [(m.start(), "do", 1) for m in self.RE_DO.finditer(data)]
        donts = [(m.start(), "don't", 1) for m in self.RE_DONT.finditer(data)]
        muls = [
            (
                m.start(),
                "mul",
                functools.reduce(lambda a, b: a * b, map(int, m.groups()), 1),
            )
            for m in self.RE_MUL.finditer(data)
        ]

        result_1 = sum(value for _, _, value in muls)

        status = "on"

        timeline = sorted(muls + does + donts)

        for _, instr, value in timeline:
            if status == "off":
                if instr == "do":
                    status = "on"
                continue

            if instr == "don't":
                status = "off"
                continue

            if instr == "mul":
                result_2 += value

        self.resolved(result_1=result_1, result_2=result_2)


solver = Solver(DAY)
solver()
