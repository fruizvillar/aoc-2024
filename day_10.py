""" Solver for AoC 2024 Day 10"""

import enum
import queue
from typing import override

import lib

DAY = int("10")


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/10"""

    class Symbol(enum.IntEnum):
        PATH_START = 0
        PATH_END = 9
        
        
    def __init__(self, day_of_month):
        super().__init__(day_of_month)
        self.maze = None

    @override
    def solve(self) -> None:

        maze = lib.Maze(register_symbol=self.Symbol.PATH_START)

        maze.load_from_pos_symbol_generator(self.read_maze_to_coords(type_=int))
        
        self.maze = maze
        
        trailheads = maze.registry[self.Symbol.PATH_START]

        th_scores = {th: self._get_trailhead_score(th) for th in trailheads}        
        self.resolved(result_1=sum(th_scores.values()))
        
        th_ratings = {th: self._get_trailhead_rating(th) for th in trailheads}        
        self.resolved(result_2=sum(th_ratings.values()))
        
        
    def _get_trailhead_score(self, trailhead: lib.Position2D) -> int:
        return self._get_th_paths(trailhead, repeat_path=False)
    
    def _get_trailhead_rating(self, trailhead: lib.Position2D) -> int:
        return self._get_th_paths(trailhead, repeat_path=True)
    
    def _get_th_paths(self, trailhead: lib.Position2D, repeat_path: bool) -> int:
        
        score = 0
        
        self.printd('Trailhead', trailhead)
        
        if self.maze[trailhead] != self.Symbol.PATH_START:
            err_msg = f'Cannot start a path from point {trailhead} != {self.Symbol.PATH_START}'
            raise RuntimeError(err_msg)

        
        q = queue.SimpleQueue() # type: queue.SimpleQueue[lib.Position2D, int ]
        
        visited = set((trailhead,))
        
        q.put_nowait((trailhead, self.Symbol.PATH_START))
        
        while not q.empty():
            
            
            step, height = q.get_nowait()
            
            
            self.printd('Q', step, height)
            
            if height == self.Symbol.PATH_END:
                score += 1
                continue
                
            
            for direction in lib.DirectionYX:
                new_step = step + direction
                
                try:
                    new_height = self.maze[new_step]
                except KeyError:
                    continue
                
                if new_height != height + 1:
                    continue
                
                if not repeat_path:
                    if new_step in visited:
                        self.printd('Visited', new_step)
                        continue
                    visited.add(new_step)
                
                self.printd('New step', new_step)
                
                q.put_nowait((new_step, new_height))
                
            self.printd('Q', q.qsize())
            
        
        
        
        return score
        


solver = Solver(DAY)
solver()
