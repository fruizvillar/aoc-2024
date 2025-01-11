""" Solver for AoC 2024 Day 11"""

import dataclasses
from typing import override

import lib

DAY = int("11")

@dataclasses.dataclass
class Stone:
    value: int
    next: "Stone" = None
    prev: "Stone" = None
    
    def blinked(self):
        new_values = self.blink_change(self.value)
        
        self.value = new_values[0]
        
        if len(new_values) == 1:
            return self.next
        
        aux = self.next
        self.next = Stone(new_values[1], prev=self, next=aux)
        
        
    @staticmethod
    def blink_change(value) -> list[int]:
        
        if value == 0:
            return [1]
        
        if (width:= len(str(value))) % 2 == 0:
            
            separator = 10 ** (width // 2)
            return [value // separator, value % separator]
            
                
        return [value * 2024]
    
    
    
# 0 -> 1 -> 2024 -> 20 --> 2 -> 4048
#                       |> 0 
#                -> 24 --> 2 -> 4048
#                       |> 4 -> 8096
class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/11"""

    @override
    def solve(self) -> None:
        
        stones = self.load_stones()
        
        for i in range(25):
            self.blink(stones)
            print(f"After {i+1} blinks: {self._count_stones(stones)}")
            if self.DEBUG:
                self._print_stones(stones)

        self.resolved(result_1=self._count_stones(stones))
        
        
        for i in range(25, 50):
            print(f"After {i+1} blinks: {self._count_stones(stones)}")
            self.blink(stones)
            if self.DEBUG:
                self._print_stones(stones)
        
        self.resolved(result_2=None)

    def blink(self, head: Stone):
        current = head

        while current:
            current = current.blinked().next
        
    
    def load_stones(self) -> Stone:
        values = list(self.read_lines_typed(int))[0]
        self.printd(values)
        
        head = current = Stone(values[0])
        
        for value in values[1:]:
            stone = Stone(value, prev=current)
            current.next = stone
            current = stone
        
        return head
    
    @staticmethod
    def _count_stones(stones: Stone) -> int:
        count = 0
        while stones:
            count += 1
            stones = stones.next
        return count
        
    @staticmethod
    def _print_stones(stones):
        while stones:
            print(stones.value, end=" ")
            stones = stones.next
        print()

solver = Solver(DAY)
solver()
