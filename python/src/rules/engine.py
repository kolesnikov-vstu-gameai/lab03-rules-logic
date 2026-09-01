"""Простой forward-chaining движок продукций над множеством фактов-кортежей."""

from dataclasses import dataclass, field
from typing import Callable

Fact = tuple


@dataclass
class Rule:
    name: str
    condition: Callable[[set[Fact]], bool]
    action: Callable[[set[Fact]], None]  # добавляет/удаляет факты
    priority: int = 0


@dataclass
class Engine:
    rules: list[Rule] = field(default_factory=list)
    facts: set[Fact] = field(default_factory=set)
    log: list[str] = field(default_factory=list)

    def add(self, rule: Rule) -> None:
        self.rules.append(rule)

    def assert_fact(self, *fact) -> None:
        self.facts.add(tuple(fact))

    def retract(self, *fact) -> None:
        self.facts.discard(tuple(fact))

    def run(self, max_cycles: int = 50) -> list[str]:
        fired: list[str] = []
        for _ in range(max_cycles):
            before = set(self.facts)
            for r in sorted(self.rules, key=lambda r: -r.priority):
                if r.condition(self.facts):
                    r.action(self.facts)
                    fired.append(r.name)
                    self.log.append(f"{r.name}: {sorted(self.facts)}")
            if self.facts == before:
                break
        return fired
