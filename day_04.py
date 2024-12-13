""" Solver for AoC 2024 Day 4"""

import collections
import dataclasses
import enum
from typing import Iterable, override

import lib

DAY = int("4")

@dataclasses.dataclass
class Position2D:
    x: int
    y: int
    
    def __add__(self, other: tuple[int, int]) -> "Position2D":
        try:
            return Position2D(self.x + other[0], self.y + other[1])
        except TypeError:
            if hasattr(other, "value"):
                other = other.value
                return self.__add__(other)
            return NotImplemented
        
    def __str__(self):
        return f"({self.x:2}, {self.y:2})"
    
    def __lt__(self, other: "Position2D"):
        return self.x <= other.x and self.y <= other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
class DirectionWithDiagonals(enum.Enum):
    UP = (-1, 0), "↑"
    DOWN = (1, 0), "↓"
    LEFT = (0, -1), "←"
    RIGHT = (0, 1), "→"
    UP_LEFT = (-1, -1), "↖"
    UP_RIGHT = (-1, 1), "↗"
    DOWN_LEFT = (1, -1), "↙"
    DOWN_RIGHT = (1, 1), "↘"
    
    
    def __new__(cls, value, repr):
        obj = object.__new__(cls,)
        obj._value_ = value
        obj.repr = repr
        return obj
    
    def __str__(self):
        return self.repr
    
    def diagonals():
        return [DirectionWithDiagonals.UP_LEFT, DirectionWithDiagonals.UP_RIGHT, 
                DirectionWithDiagonals.DOWN_LEFT, DirectionWithDiagonals.DOWN_RIGHT]


DEBUG = False

def printd(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/4"""

    @override
    def solve(self) -> None:
        tick = "🎄"
        
        soup = [list(line[0]) for line in self.read_lines_typed(str)]
        self.soup = soup
        n_xmas = 0
        
        for x_pos in self.find_xmas_x():
            
            printd()
            printd("X___", x_pos, '+')
            
            for m_pos, direction in self.find_xmas_m(x_pos):
                printd("XM__", m_pos, direction)
                if a_pos := self.is_xmas_a(m_pos, direction):
                    printd("XMA_", a_pos, direction)
                    if s_pos:= self.is_xmas_s(a_pos, direction):
                        printd("XMAS", s_pos, direction, tick)
                        n_xmas += 1
        
                

        self.resolved(result_1=n_xmas)
        
        n_x_mas = 0
        
        mas_occurencies = []
        
        for m_pos in self.find_x_mas_m():
            
            printd("M__", m_pos)
            for a_pos, direction in self.find_x_mas_a(m_pos):
                printd("MA_", a_pos, direction)
                if s_pos := self.is_x_mas_s(a_pos, direction):
                    printd("MAS", s_pos, direction, tick)
                    mas_occurencies.append((m_pos, a_pos, s_pos))
                    
        mas_occurencies.sort(key=lambda x: x[1])
        a_locations = collections.Counter(a_pos for _, a_pos, _ in mas_occurencies)
        
        for a_location, count in a_locations.items():
            if count == 2:
                printd(f"A is in two MAS in {a_location}")
                n_x_mas += 1
                continue
            if count == 3:
                raise ValueError(f"A is in three MAS in {a_location}")
                
        self.resolved(result_2=n_x_mas)
        
    def find_xmas_x(self) -> Iterable[Position2D]:
        """Part 1.1: finding the X in XMAS"""
        yield from self.find_letter("X")
        
    def find_xmas_m(self, x_pos: Position2D) -> Iterable[tuple[Position2D, DirectionWithDiagonals]]:
        """Part 1.2: finding the M in XMAS (starting from X)"""	
        
        for direction in DirectionWithDiagonals:
            m_pos = x_pos + direction
            if self.letter_in(m_pos) == "M":
                yield m_pos, direction
            
    def is_xmas_a(self, m_pos: Position2D, direction: DirectionWithDiagonals) -> Position2D | None:
        """Part 1.3: continuing in `direction` from M to ensure that there is an A"""
        a_pos = m_pos + direction
        if self.letter_in(a_pos) == "A":
            return a_pos
            
            
    def is_xmas_s(self, a_pos: Position2D, direction: DirectionWithDiagonals) ->  Position2D | None:
        """Part 1.4: continuing in `direction` from A to ensure that there is an S"""
        s_pos = a_pos + direction
        if self.letter_in(s_pos) == "S":
            return s_pos
    
        
        
    def find_x_mas_m(self) -> Iterable[Position2D]:
        """Part 2.1: finding the M in X-MAS
        M S
         A
        M S
        """
        for m_pos in self.find_letter("M"):
            yield m_pos
        
    def find_x_mas_a(self, m_pos: Position2D) -> Iterable[tuple[Position2D, DirectionWithDiagonals]]:
        """Part 2.2: finding the A in X-MAS
        M S                M M
         A    (or)          A    (or ...)
        M S                S S
        """
        for direction in DirectionWithDiagonals.diagonals():
            a_pos = m_pos + direction
            if self.letter_in(a_pos) == "A":
                yield a_pos, direction
                
                
    def is_x_mas_s(self, a_pos: Position2D, direction: DirectionWithDiagonals) -> Position2D | None:
        """Part 2.3: finding the S in X-MAS"""
        return self.is_xmas_s(a_pos, direction) 
    
        
    def find_letter(self, letter) -> Iterable[Position2D]:
        for i in range(len(self.soup)):
            for j in range(len(self.soup[i])):
                if self.soup[i][j] == letter:
                    yield Position2D(i, j)
    
    def letter_in(self, pos: Position2D) -> str | None:
        if pos.x < 0 or pos.y < 0:
            return None
        try:
            return self.soup[pos.x][pos.y]
            
        except IndexError:
            return None
    
        
        




































solver = Solver(DAY)
solver()
