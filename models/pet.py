from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.species}, age {self.age})"
