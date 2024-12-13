""" Solver for AoC 2024 Day XX-DAY-XX"""

from typing import override

import lib

DAY = int("XX-DAY-XX")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/XX-DAY-XX"""

    @override
    def solve(self) -> None:

        self.resolved(result_1=None)
        self.resolved(result_2=None)


solver = Solver(DAY)
solver()
