
from collections import Counter
import lib
from typing import override

DAY = 'XX-DAY-XX'

class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/XX-DAY-XX"""
    @override
    def solve(self) -> None:
        
        self.resolved(result_1=None)
        self.resolved(result_2=None)
        
        
        
solver = Solver(DAY)
solver()
