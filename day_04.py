""" Solver for AoC 2024 Day 4"""

import collections
from typing import Iterable, override

import lib

DAY = int("4")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/4"""

    @override
    def solve(self) -> None:
        tick = "🎄"

        soup = [list(line[0]) for line in self.read_lines_typed(str)]
        self.soup = soup
        n_xmas = 0

        for x_pos in self.find_xmas_x():

            self.printd()
            self.printd("X___", x_pos, "+")

            for m_pos, direction in self.find_xmas_m(x_pos):
                self.printd("XM__", m_pos, direction)
                if a_pos := self.is_xmas_a(m_pos, direction):
                    self.printd("XMA_", a_pos, direction)
                    if s_pos := self.is_xmas_s(a_pos, direction):
                        self.printd("XMAS", s_pos, direction, tick)
                        n_xmas += 1

        self.resolved(result_1=n_xmas)

        n_x_mas = 0

        mas_occurencies = []

        for m_pos in self.find_x_mas_m():

            self.printd("M__", m_pos)
            for a_pos, direction in self.find_x_mas_a(m_pos):
                self.printd("MA_", a_pos, direction)
                if s_pos := self.is_x_mas_s(a_pos, direction):
                    self.printd("MAS", s_pos, direction, tick)
                    mas_occurencies.append((m_pos, a_pos, s_pos))

        mas_occurencies.sort(key=lambda x: x[1])
        a_locations = collections.Counter(a_pos for _, a_pos, _ in mas_occurencies)
        print(a_locations)
        for a_location, count in a_locations.items():
            if count == 2:
                self.printd(f"A is in two MAS in {a_location}")
                n_x_mas += 1
                continue
            if count == 3:
                raise ValueError(f"A is in three MAS in {a_location}")

        self.resolved(result_2=n_x_mas)

    def find_xmas_x(self) -> Iterable[lib.Position2D]:
        """Part 1.1: finding the X in XMAS"""
        yield from self.find_letter("X")

    def find_xmas_m(
        self, x_pos: lib.Position2D
    ) -> Iterable[tuple[lib.Position2D, lib.DirectionWithDiagonalsType]]:
        """Part 1.2: finding the M in XMAS (starting from X)"""

        for direction in lib.directions_with_diagonals():
            m_pos = x_pos + direction
            if self.letter_in(m_pos) == "M":
                yield m_pos, direction

    def is_xmas_a(
        self, m_pos: lib.Position2D, direction: lib.DirectionWithDiagonalsType
    ) -> lib.Position2D | None:
        """Part 1.3: continuing in `direction` from M to ensure that there is an A"""
        a_pos = m_pos + direction
        if self.letter_in(a_pos) == "A":
            return a_pos

    def is_xmas_s(
        self, a_pos: lib.Position2D, direction: lib.DirectionWithDiagonalsType
    ) -> lib.Position2D | None:
        """Part 1.4: continuing in `direction` from A to ensure that there is an S"""
        s_pos = a_pos + direction
        if self.letter_in(s_pos) == "S":
            return s_pos

    def find_x_mas_m(self) -> Iterable[lib.Position2D]:
        """Part 2.1: finding the M in X-MAS
        M S
         A
        M S
        """
        for m_pos in self.find_letter("M"):
            yield m_pos

    def find_x_mas_a(
        self, m_pos: lib.Position2D
    ) -> Iterable[tuple[lib.Position2D, lib.DirectionWithDiagonalsType]]:
        """Part 2.2: finding the A in X-MAS
        M S                M M
         A    (or)          A    (or ...)
        M S                S S
        """
        for direction_diagonal in lib.DirectionDiagonals:
            a_pos = m_pos + direction_diagonal
            if self.letter_in(a_pos) == "A":
                yield a_pos, direction_diagonal

    def is_x_mas_s(
        self, a_pos: lib.Position2D, direction: lib.DirectionWithDiagonalsType
    ) -> lib.Position2D | None:
        """Part 2.3: finding the S in X-MAS"""
        return self.is_xmas_s(a_pos, direction)

    def find_letter(self, letter) -> Iterable[lib.Position2D]:
        for i in range(len(self.soup)):
            for j in range(len(self.soup[i])):
                if self.soup[i][j] == letter:
                    yield lib.Position2D(i, j)

    def letter_in(self, pos: lib.Position2D) -> str | None:
        if pos.x < 0 or pos.y < 0:
            return None
        try:
            return self.soup[pos.x][pos.y]

        except IndexError:
            return None


solver = Solver(DAY)
solver()
