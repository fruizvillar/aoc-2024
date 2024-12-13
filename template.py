""" Solver for AoC 2024 Day XX-DAY-XX"""

import lib
from typing import override

DAY = int("XX-DAY-XX")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/XX-DAY-XX"""

    @override
    def solve(self) -> None:

        self.resolved(result_1=None)
        self.resolved(result_2=None)


solver = Solver(DAY)
solver()
