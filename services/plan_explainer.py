from __future__ import annotations
from models import Owner, Pet, ScheduledTask, Task


class PlanExplainer:
    def __init__(
        self,
        scheduled_tasks: list[ScheduledTask],
        skipped_tasks: list[Task],
        owner: Owner,
        pet: Pet,
    ) -> None:
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.owner = owner
        self.pet = pet
        self.total_minutes_scheduled = sum(
            st.task.duration_minutes for st in scheduled_tasks
        )

    def summarize(self) -> str:
        n = len(self.scheduled_tasks)
        s = len(self.skipped_tasks)
        return (
            f"Plan for **{self.pet.name}** ({self.owner.name}): "
            f"{n} task(s) scheduled totalling {self.total_minutes_scheduled} min. "
            f"{s} task(s) skipped due to time constraints."
        )

    def explain_task(self, st: ScheduledTask) -> str:
        return (
            f"**{st.task.title}** — {st.start_time} to {st.end_time}. "
            f"{st.reason}"
        )

    def explain_skipped(self) -> str:
        if not self.skipped_tasks:
            return "All tasks fit within the available time window."
        names = ", ".join(t.title for t in self.skipped_tasks)
        return (
            f"The following task(s) were skipped because there wasn't enough time: "
            f"{names}. Consider reducing durations or increasing available time."
        )
