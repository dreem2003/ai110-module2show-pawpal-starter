from __future__ import annotations
from dataclasses import dataclass, field
from models.pet import Pet


@dataclass
class Owner:
    name: str
    available_minutes: int = 480  # default: 8 hours
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def __str__(self) -> str:
        return f"{self.name} ({self.available_minutes} min available)"
