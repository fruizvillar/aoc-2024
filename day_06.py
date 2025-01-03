""" Solver for AoC 2024 Day 6"""

import collections
import enum
from typing import Tuple, override

import colorama

import lib

DAY = int("6")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/6"""

    GUARD_DIRECTION_START = lib.DirectionYX.UP

    class Symbol(enum.StrEnum):
        WALL = "#"
        EMPTY = "."
        GUARD = "^"
        VISITED = "X"
        LOOP_OPTION = "O"

    _PRINT_COLOURS = {
        Symbol.WALL: colorama.Fore.RED,
        Symbol.EMPTY: colorama.Fore.WHITE,
        Symbol.GUARD: colorama.Fore.GREEN,
        Symbol.VISITED: colorama.Fore.BLUE,
        Symbol.LOOP_OPTION: colorama.Fore.YELLOW,
    }

    _D_ORDER = lib.DirectionYX.cycle(order="CW")
    _D_ITER = lib.DirectionYX.cycle(start=GUARD_DIRECTION_START, order="CW")

    def next_direction(self, d=None):
        if d is None:
            return next(self._D_ITER)

        while next(self._D_ORDER) != d:
            pass
        return next(self._D_ORDER)

    def load_maze(self) -> lib.Maze:
        maze = lib.Maze(idx_symbol=self.Symbol.WALL, register_symbol=self.Symbol.GUARD)

        maze.load_from_pos_simbol_generator(
            self.read_maze_to_coords(ignore_symbol=self.Symbol.EMPTY)
        )

        maze.set_colours(self._PRINT_COLOURS)

        return maze

    def guard_pos_init(self, maze: Maze):
        pos = maze.registry[self.Symbol.GUARD]

        if not pos:
            raise RuntimeError("Guard not found")
        if len(pos) > 1:
            raise RuntimeError("Multiple guards found")
        pos = pos[0]
        maze.maze[pos] = self.Symbol.EMPTY
        return pos

    @override
    def solve(self) -> None:

        maze = self.load_maze()

        guard_pos = self.guard_pos_init(maze)
        guard_direction = self.next_direction()

        visited_pos = collections.defaultdict(list)
        visited_pos[guard_pos].append(guard_direction)

        loop_options = set()

        while guard_pos in maze:
            maze.print(
                replace={
                    guard_pos: self.Symbol.GUARD,
                }
            )
            print(guard_pos, guard_direction)
            walked, some_loop_options = self.analyse_line(
                maze, p0=guard_pos, d=guard_direction, previously_walked=visited_pos
            )

            loop_options.update(some_loop_options)

            guard_pos = walked[-1]
            for p in walked:
                visited_pos[p].append(guard_direction)

            if not guard_pos:
                break

            guard_direction = self.next_direction()

        print(sorted(visited_pos))
        maze.print(
            replace={p: "X" for p in visited_pos} | {p: "O" for p in loop_options}
        )
        self.resolved(result_1=len(visited_pos) - 1, result_2=len(loop_options))

    def analyse_line(
        self,
        maze: Maze,
        p0: lib.Position2D,
        d: lib.DirectionYX,
        previously_walked: dict[lib.Position2D, list[lib.DirectionYX]] = None,
    ) -> Tuple[lib.Position2D, lib.Position2D]:

        if self.Symbol.WALL != maze.idx_symbol:
            raise ValueError("Symbol must be the one used to index the maze")

        if d.x and d.y:
            raise ValueError("Direction must be parallel to X-axis or Y-axis")

        if not d.x and not d.y:
            raise ValueError("Direction cannot be 0\u20D7")

        if d.x:
            # We're moving in the X-axis, Y is fixed.
            obstacles_in_line = maze.idx_y[p0.y]

        if d.y:
            obstacles_in_line = maze.idx_x[p0.x]

        p = p0

        walked = []
        obstacle_loop_option = []

        d_after_obstacle = self.next_direction(d)

        while p in maze:

            p_next = p + d
            p_alt = p + d_after_obstacle

            if p_alt in previously_walked:
                # THere could be a loop
                walked_route_directions = previously_walked[p_alt]
                if d_after_obstacle in walked_route_directions:
                    # We've already walked this route, in this direction, so loop found
                    obstacle_loop_option.append(p_next)

            if p_next in obstacles_in_line:
                break

            walked.append(p_next)
            p = p_next

        return walked, obstacle_loop_option


solver = Solver(DAY)
solver()
