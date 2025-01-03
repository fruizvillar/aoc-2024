""" Solver for AoC 2024 Day 8"""

import collections
import enum
import itertools
from typing import override

import lib

DAY = int("8")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/8"""

    class Symbol(enum.StrEnum):
        ANTENNA = "A"
        EMPTY = "."
        ANTI_NODE = "#"

    @override
    def solve(self) -> None:

        frequencies_and_locations = collections.defaultdict(set)

        maze = lib.Maze(register_symbol="ALL")

        maze.load_from_pos_simbol_generator(
            self.read_maze_to_coords(), ignore_symbol=self.Symbol.EMPTY
        )

        for antenna_pos, freq in self.read_maze_to_coords(ignore_symbol="."):
            frequencies_and_locations[freq].add(antenna_pos)

        self.DEBUG = True
        antinodes_per_f = self.find_all_antinodes(frequencies_and_locations, maze)

        if self.DEBUG:
            for f, antinodes in antinodes_per_f.items():
                print(f"Frequency {f} at locations {frequencies_and_locations[f]}: {antinodes}")

        antinodes = set(itertools.chain(*antinodes_per_f.values()))

        maze.print(replace={x: self.Symbol.ANTI_NODE for x in antinodes})

        self.resolved(result_1=len(antinodes))
        
        antinodes_per_f = self.find_all_antinodes(frequencies_and_locations, maze, multiple_harmonics=True)
        antinodes = set(itertools.chain(*antinodes_per_f.values()))
        
        antinodes |= set(itertools.chain(*frequencies_and_locations.values()))

        maze.print(replace={x: self.Symbol.ANTI_NODE for x in antinodes})

        self.resolved(result_2=len(antinodes))

    def find_all_antinodes(self, frequencies_and_locations, maze:lib.Maze, multiple_harmonics=False) -> dict[int, set[lib.Position2D]]:
        antinodes = {}
        for f, locs in frequencies_and_locations.items():

            antinodes[f] = self.find_antinodes(locs,maze, multiple_harmonics)
          
        return antinodes

    def find_antinodes(self, nodes, maze: lib.Maze, multiple_harmonics) -> set[lib.Position2D]:
        antinodes = set()
        for node_pair in itertools.combinations(nodes, 2):
            antinodes |= self.calc_antinodes(*node_pair, maze, multiple_harmonics=multiple_harmonics)
         

        return antinodes

    def calc_antinodes(
        self, a: lib.Position2D, b: lib.Position2D, maze, multiple_harmonics=False
    ) -> set[lib.Position2D]:
        """Calculate the antinodes between two nodes
        A=(1,3), B=(3,1) --> D=(2,-2)  --> AN1=(2,1), AN2=(2,3)
        """
        if a == b:
            return set()

        diff = b - a
        
        antinodes = []
        
        while (b := b + diff) in maze:
            antinodes.append(b)
            
            if not multiple_harmonics:
                break
            
        while (a:= a - diff) in maze:
            antinodes.append(a)
            
            if not multiple_harmonics:
                break
            

        return set(antinodes)


solver = Solver(DAY)
solver()
