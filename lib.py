
import pathlib
import abc

INPUTS = pathlib.Path('inputs')

class Solver(abc.ABC):
    def __init__(self, day_of_month):
        self.day_of_month = day_of_month
        
        self.filename = INPUTS / f'day_{day_of_month:02}.txt'
        
        self.result_1 = self.result_2 = None


    def read_lines_typed(self, type_):
        with self.filename.open() as f:
            for line in f.readlines():
                yield tuple(map(type_, line.strip().split()))

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
                
    def __call__(self):
        self.solve()
        
        if self.result_1 is None:
            print("Result 1: Not resolved")
        if self.result_2 is None:
            print("Result 2: Not resolved")
        

