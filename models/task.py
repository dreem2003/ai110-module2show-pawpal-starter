from __future__ import annotations
from dataclasses import dataclass
from models.priority import Priority


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    category: str = "general"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def __str__(self) -> str:
        return f"[{self.priority.name}] {self.title} ({self.duration_minutes} min)"


@dataclass
class ScheduledTask:
    task: Task
    start_time: str   # "HH:MM"
    end_time: str     # "HH:MM"
    reason: str = ""
