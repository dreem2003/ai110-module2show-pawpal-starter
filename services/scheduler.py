from __future__ import annotations
from models import Owner, Pet, Task, ScheduledTask


def _minutes_to_time(minutes: int) -> str:
    """Convert an absolute minute count (from midnight) to 'HH:MM' string."""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


class Scheduler:
    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        day_start_minute: int = 480,   # 08:00
        day_end_minute: int = 1320,    # 22:00
    ) -> None:
        self.owner = owner
        self.pet = pet
        self.day_start_minute = day_start_minute
        self.day_end_minute = day_end_minute
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        self.tasks = [t for t in self.tasks if t.title != title]

    def generate_plan(self) -> tuple[list[ScheduledTask], list[Task]]:
        """
        Sort tasks by priority (HIGH first), then schedule them
        sequentially within the available day window.

        Returns a tuple of (scheduled_tasks, skipped_tasks).
        """
        window_minutes = min(
            self.owner.available_minutes,
            self.day_end_minute - self.day_start_minute,
        )

        sorted_tasks = sorted(
            [t for t in self.tasks if not t.completed],
            key=self._priority_sort_key,
            reverse=True,
        )

        scheduled: list[ScheduledTask] = []
        skipped: list[Task] = []
        current_minute = self.day_start_minute
        remaining = window_minutes

        for task in sorted_tasks:
            if self._fits_in_window(task, remaining):
                start = _minutes_to_time(current_minute)
                end = _minutes_to_time(current_minute + task.duration_minutes)
                reason = self._build_reason(task, len(scheduled) + 1)
                scheduled.append(ScheduledTask(task, start, end, reason))
                current_minute += task.duration_minutes
                remaining -= task.duration_minutes
            else:
                skipped.append(task)

        return scheduled, skipped

    def _fits_in_window(self, task: Task, remaining_minutes: int) -> bool:
        return task.duration_minutes <= remaining_minutes

    @staticmethod
    def _priority_sort_key(task: Task) -> int:
        return task.priority.value

    @staticmethod
    def _build_reason(task: Task, position: int) -> str:
        ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(position, f"{position}th")
        return (
            f"Scheduled {ordinal} — {task.priority.name.capitalize()} priority "
            f"{task.category} task ({task.duration_minutes} min)."
        )
