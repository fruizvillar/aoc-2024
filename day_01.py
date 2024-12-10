
from collections import Counter
import lib
from typing import override

DAY = 1

class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/2"""
    @override
    def solve(self):
        a0 = []
        a1 = []
            
        for n0, n1 in self.read_lines_typed(int):
            a0.append(n0)
            a1.append(n1)
        
        result_1 = sum( abs(a-b) for (a, b) in zip(sorted(a0), sorted(a1)))
        
        self.resolved(result_1=result_1)
        result_2 = 0
        
        count_1 = Counter(a1)
        
        for n in a0:
            if occurencies := count_1.get(n, 0):
                result_2 += n * occurencies
        
        self.resolved(result_2=result_2)
        
        
        
solver = Solver(DAY)
solver()
