
import datetime
import pathlib
import sys

import lib

F_SOLUTION_TEMPLATE = pathlib.Path(__file__).parent / 'template.py'

def main():
    try:
        day = int(sys.argv[1])
    except (IndexError, ValueError):
        day = guess_day()


    create_files(day)


def guess_day() -> int:
    date = datetime.datetime.now().date()
    
    if date.month != 12:
        raise ValueError("Could not use today as day of AoC: Not in December!")
    
    if date.day > 25:
        raise ValueError("Could not use today as day of AoC: After 25th!")
    
    return date.day


def create_files(day: int):
  
        
    lib.INPUTS.mkdir(exist_ok=True)
    f_in = lib.INPUTS / f'day_{day:02}.txt'
    
    f_in = f_in.absolute()
    
    if f_in.exists():
        print(f"File {f_in.as_uri()} already exists")
    else:
        f_in.touch()
        print(f"Created input file {f_in.as_uri()}")
    
    
    f_solution = pathlib.Path(__file__).parent / f'day_{day:02}.py'
    if f_solution.exists():
        print(f"File {f_solution.as_uri()} already exists")
    else:
        with F_SOLUTION_TEMPLATE.open() as f:
            template = f.read()
        
        with f_solution.open('w') as f:
            f.write(template.replace('XX-DAY-XX', str(day)))
        
        print(f"Created solution file {f_solution.as_uri()} from template {F_SOLUTION_TEMPLATE}")



if __name__ == '__main__':
    main()
