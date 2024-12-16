""" Solver for AoC 2024 Day 5"""

import collections
from typing import override
import dataclasses
import lib

DAY = int("5")

@dataclasses.dataclass
class PageOrderRule:
    predecesor: int
    ref: int
    
    def __repr__(self):
        return f"|{self.predecesor:2d} → {self.ref:2d}|"
    
@dataclasses.dataclass
class ManualUpdate:
    pages: list[int]
    mid: int = 0
    def __post_init__(self):
        midpoint = len(self.pages) // 2
        self.mid = self.pages[midpoint]
    
@dataclasses.dataclass
class PageNode:
    n: int
    prev: "PageNode" = dataclasses.field(default=None, compare=False, repr=False)
    next: "PageNode" = dataclasses.field(default=None, compare=False, repr=False)
    
    def __hash__(self):
        return hash(self.n)
    
    
class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/5"""
    
    @override
    def solve(self) -> None:
                
        rules = []
        updates = []
        
        data = self.read()

        for line in data.splitlines():
            if "|" in line:
                ref, predecesor = map(int, line.strip().split("|"))
                rules.append(PageOrderRule(ref, predecesor))
                continue
            
            if "," in line:
                pages = list(map(int, line.split(",")))
                updates.append(ManualUpdate(pages))
                continue
            
            if line.strip():
                raise ValueError(f"Invalid line: {line}")
    
        

        valid_updates = 0
        
        corrected_updates = 0
        
        for update in updates:
            self.printd(f"Update: {update.pages}")
            applicable_rules = collections.defaultdict(list)

            for rule in rules:
                if rule.ref in update.pages and rule.predecesor in update.pages:
                    applicable_rules[rule.ref].append(rule)
            
            self.printd(f"Applicable rules: {len(applicable_rules)=}")
                
            if self.verify_update(update, applicable_rules):
                valid_updates += update.mid
                continue

            corrected_updates += self.reshuffle_update(update, applicable_rules)

        self.resolved(result_1=valid_updates, result_2=corrected_updates)
        
        
        
    def verify_update(self, update: ManualUpdate, rules: dict[int, list[PageOrderRule]]) -> bool:
        
        added_pages = set()
        for page in update.pages:
            
            added_pages.add(page)

            if page not in rules:
                continue
                
            for rule in rules[page]:
                if rule.predecesor not in added_pages:
                    return False
        
        return True

    def reshuffle_update(self, update: ManualUpdate, rules: dict[int, list[PageOrderRule]]) -> ManualUpdate:
        
        corrected_pages = []
        changed = True
        
        while len(corrected_pages) < len(update.pages) and changed:
            changed = False

            for page in update.pages:
                if page in corrected_pages:
                    continue
                
                if page not in rules:
                    corrected_pages.append(page)
                    changed = True
                    continue

                all_rules_fulfilled = True                
                for rule in rules[page]:
                    if rule.predecesor in update.pages and rule.predecesor not in corrected_pages:
                        self.printd(f"Page {page:2d}. Awaiting: {rule.predecesor=} not added yet")
                        all_rules_fulfilled = False
                        break
                    
                if all_rules_fulfilled:
                    corrected_pages.append(page)
                    changed = True
        

        if not changed:
            raise RuntimeError("Could not correct update")
    
        return ManualUpdate(corrected_pages).mid
    
            
        

solver = Solver(DAY)
solver()
