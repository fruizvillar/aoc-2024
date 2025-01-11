import abc
import collections
import enum
import itertools
import math
import pathlib
import re
from typing import Any, Iterable, Union

import colorama

colorama.init(convert=True)

INPUTS = pathlib.Path("inputs")
RESULTS = pathlib.Path("results")
SOLUTIONS = pathlib.Path(__file__).parent

URL = "https://adventofcode.com/2024"


class Solver(abc.ABC):
    DEBUG = False

    def __init__(self, day_of_month):
        self.day_of_month = day_of_month

        self.filename = INPUTS / f"day_{day_of_month:02}.txt"

        self.result_1 = self.result_2 = None

    def read(self):
        with self.filename.open() as f:
            return f.read()

    def read_lines_typed(self, type_, sep=None):
        with self.filename.open() as f:
            for line in f.readlines():
                yield tuple(map(type_, line.strip().split(sep)))

    def read_lines_re(self, pattern, type_=None, split=False):
        with self.filename.open() as f:
            for line in f.readlines():
                raw = line.strip()

                if split:
                    matched_bits = re.split(pattern, raw)
                else:
                    matched_bits = re.match(pattern, raw).groups()

                if type_:
                    yield tuple(type_(g) for g in matched_bits if g)
                else:
                    yield matched_bits

    def read_maze_to_coords(self, ignore_symbol=None, type_=str):
        with self.filename.open() as f:
            for y, line in enumerate(f.readlines()):
                for x, symbol in enumerate(line.strip()):
                    if symbol != ignore_symbol:
                        yield Position2D(x, y), type_(symbol)

    @abc.abstractmethod
    def solve(self) -> None:
        raise NotImplementedError

    def resolved(self, *, result_1=None, result_2=None):
        if result_1 is not None:
            self.result_1 = result_1
            print(f"Result 1: {result_1}")

        if result_2 is not None:
            self.result_2 = result_2
            print(f"Result 2: {result_2}")

        for i, result in enumerate((result_1, result_2), 1):
            if result is None:
                continue

            if (f_result := (RESULTS / f"day_{self.day_of_month:02}_{i}.txt")).exists():
                with f_result.open() as f:
                    if (saved_result := f.read().strip()) == str(result):
                        print(f"Result {i} already exists and matches")
                        continue

                    print(
                        f"Result {i} already exists but does not match ({saved_result=}, {result=})"
                    )
                    to_save = self._ask_user_yn_safe(f"Overwrite result {i}?")

            else:
                to_save = self._ask_user_yn_safe(f"Save result {i}?")

            if to_save:
                with f_result.open("w") as f:
                    f.write(str(result))
                    
    def _ask_user_yn_safe(self, prompt: str, default: bool=False) -> bool:
        try:
            reply = input(prompt + ' (y/N) ').lower()
        except KeyboardInterrupt:
            print('Ctrl-C detected. Cancelling.')
            return default

        return reply == 'y'

    def __call__(self):
        self.solve()

        if self.result_1 is None:
            print("Result 1: Not resolved")
        if self.result_2 is None:
            print("Result 2: Not resolved")

    def printd(self, *args, **kwargs):
        if self.DEBUG:
            print(*args, **kwargs)


class Position2D:
    x: int
    y: int

    def __init__(self, x: int, y: int | None = None):
        if isinstance(x, int):
            if y is None:
                raise ValueError("y must be provided")
            self.x = x
            self.y = y
            return

        if isinstance(x, DirectionWithReprEnum):
            self.x, self.y = x.value.x, x.value.y
            return

        try:
            self.x, self.y = tuple(x)
        except TypeError:
            try:
                self.x, self.y = x.x, x.y
            except AttributeError:

                raise ValueError("x must be a tuple or two integers")

    def __add__(self, other: Union[tuple[int, int], "Position2D"]) -> "Position2D":
        try:
            return Position2D(x=self.x + other.x, y=self.y + other.y)
        except TypeError:
            pass
        try:
            return Position2D(self.x + other[0], self.y + other[1])
        except TypeError:
            pass

        try:
            return Position2D(self.x + other[0], self.y + other[1])
        except TypeError:
            pass

        if hasattr(other, "value"):
            return self.__add__(other.value)

        return NotImplemented

    def __sub__(self, other: Union[tuple[int, int], "Position2D"]) -> "Position2D":
        try:
            return Position2D(x=self.x - other.x, y=self.y - other.y)
        except TypeError:
            pass
        try:
            return Position2D(self.x - other[0], self.y - other[1])
        except TypeError:
            pass

        try:
            return Position2D(self.x - other[0], self.y - other[1])
        except TypeError:
            pass

        if hasattr(other, "value"):
            return self.__sub__(other.value)

        return NotImplemented

    def angle_diff(self, other: "Position2D") -> float:
        if not isinstance(other, (Position2D, DirectionYX)):
            try:
                other = Position2D(other)
            except ValueError:
                raise TypeError(f"Expected Position2D, got {type(other)}")
        return self.angle - other.angle

    @property
    def angle(self) -> float:
        v_minus_pi_to_pi = self._angle_minus_pi_to_pi()
        return (
            v_minus_pi_to_pi
            if v_minus_pi_to_pi >= 0
            else 2 * math.pi + v_minus_pi_to_pi
        )

    def _angle_minus_pi_to_pi(self) -> float:
        """Angle in radians from the X-axis+. Range: −π ≤ α ≤ π."""
        return math.atan2(-self.y, self.x)

    def __str__(self):
        return f"P({self.x:2}, {self.y:2})"

    def __repr__(self):
        return str(self)

    def __lt__(self, other: "Position2D"):
        return self.x <= other.x and self.y <= other.y

    def __eq__(self, other: "Position2D"):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class DirectionWithReprEnum(enum.Enum):
    def __new__(cls, value, repr):
        obj = object.__new__(
            cls,
        )
        obj._value_ = value
        obj.repr = repr
        return obj

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, value):
        return self.value == value

    def __iter__(self):
        return iter(self.value)

    def __str__(self):
        return f"D_{self.name}"

    def __repr__(self):
        return str(self)

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return self.value.__getattribute__(name)

    @classmethod
    def cycle(cls, start=None, order="CCW", once=False):
        items = list(cls)

        if not items:
            return iter([])

        if start is None:
            start = items[0]

        if order == "CW":
            reverse = True
        elif order == "CCW":
            reverse = False
        else:
            raise NotImplementedError(f"Unknown order: {order}")

        series = sorted(items, key=lambda d: d.value.angle, reverse=reverse)

        while series[0] != start:
            series.append(series.pop(0))

        print("Sorted series")
        for d in series:
            print(d, d.value.angle, d.value.angle_diff(start))
        if once:
            return iter(series)

        return itertools.cycle(series)


class DirectionYX(DirectionWithReprEnum):
    UP = Position2D(0, -1), "↑"
    RIGHT = Position2D(1, 0), "→"
    DOWN = Position2D(-1, 0), "↓"
    LEFT = Position2D(0, 1), "←"


class DirectionDiagonals(DirectionWithReprEnum):
    UP_LEFT = Position2D(-1, -1), "↖"
    UP_RIGHT = Position2D(1, -1), "↗"
    DOWN_LEFT = Position2D(-1, 1), "↙"
    DOWN_RIGHT = Position2D(1, 1), "↘"


type DirectionWithDiagonalsType = DirectionYX | DirectionDiagonals


def directions_with_diagonals(order="cycle_from_up_left"):
    if order == "cycle_from_up_left":
        return (
            DirectionDiagonals.UP_LEFT,
            DirectionYX.UP,
            DirectionDiagonals.UP_RIGHT,
            DirectionYX.RIGHT,
            DirectionDiagonals.DOWN_RIGHT,
            DirectionYX.DOWN,
            DirectionDiagonals.DOWN_LEFT,
            DirectionYX.LEFT,
        )

    if order == "xy_first":
        return tuple(list(DirectionYX) + list(DirectionDiagonals))

    raise NotImplementedError(f"Unknown order: {order}")


class Maze:
    DEBUG = False

    def __init__(
        self, idx_symbol: str | None = None, register_symbol: str | None = None
    ):
        self.maze = {}
        self.idx_x = collections.defaultdict(list)
        self.idx_y = collections.defaultdict(list)
        self.registry = collections.defaultdict(list)
        self.w = self.h = 0
        self.idx_symbol = idx_symbol
        self.register_symbol = register_symbol
        self._colours = {}

    def load_from_pos_symbol_generator(
        self, pos_symbol_gen: Iterable[tuple[Position2D, Any]], ignore_symbol=None
    ):
        ignore_symbol = ignore_symbol or {}
        max_x = max_y = 0

        for pos, symbol in pos_symbol_gen:
            max_x = max(max_x, pos.x)
            max_y = max(max_y, pos.y)

            if symbol == ignore_symbol or symbol in ignore_symbol:
                continue
            if self.DEBUG:
                print(pos, symbol)
            self.maze[pos] = symbol

            if (
                symbol == self.register_symbol
                or (hasattr(self.register_symbol, '__iter__') and symbol in self.register_symbol)
                or self.register_symbol == "ALL"
            ):
                self.registry[symbol].append(pos)

            if self.idx_symbol == symbol:
                self.idx_x[pos.x].append(pos)
                self.idx_y[pos.y].append(pos)

        self.h = max_y + 1
        self.w = max_x + 1

    def print(self, replace: dict[Position2D, str] = None):
        if not replace:
            replace = {}

        print("Maze:", self.h, self.w)
        for y in range(self.h):
            for x in range(self.w):
                pos = Position2D(x, y)

                if replacement := replace.get(pos, None):
                    print(self.colour(replacement), end="")
                else:
                    print(self.get_with_c(pos, "."), end="")
            print()

    def get_with_c(self, pos: Position2D, default: str = None):
        symbol = self.maze.get(pos, default)
        return self.colour(symbol)

    def colour(self, symbol: str):
        colour = self._colours.get(symbol, colorama.Fore.WHITE)
        return colour + symbol + colorama.Fore.RESET

    def set_colours(self, colours: dict[str, str]):
        self._colours |= colours

    def __contains__(self, pos: Position2D):
        return 0 <= pos.y < self.h and 0 <= pos.x < self.w
    
    def __getitem__(self, pos: Position2D):
        return self.maze[pos]

    def __setitem__(self, pos: Position2D, value: Any):
        self.maze[pos] = value

    def __delitem__(self, pos: Position2D):
        del self.maze[pos]
