"""Integration tests: end-to-end connections between models, services, and utils."""
import pytest
from models import Owner, Pet, Task, Priority
from services import Scheduler, PlanExplainer
from utils import parse_priority
from constants import SAMPLE_TASKS


# ── Full scheduling flow ───────────────────────────────────────────────────────

class TestFullFlow:
    def test_scheduler_output_feeds_plan_explainer(self):
        """Scheduler output (scheduled, skipped) connects directly to PlanExplainer."""
        owner = Owner("Jordan", available_minutes=480)
        pet = Pet("Mochi", "dog", age=3)
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.add_task(Task("Walk", 30, Priority.HIGH, "exercise"))
        scheduler.add_task(Task("Feed", 10, Priority.HIGH, "feeding"))

        scheduled, skipped = scheduler.generate_plan()
        explainer = PlanExplainer(scheduled, skipped, owner, pet)

        summary = explainer.summarize()
        assert "Mochi" in summary
        assert "Jordan" in summary
        assert "2" in summary  # 2 tasks scheduled

    def test_parse_priority_result_used_in_task_and_scheduler(self):
        """utils.parse_priority output flows correctly into Task → Scheduler."""
        owner = Owner("Sam", available_minutes=120)
        pet = Pet("Luna", "cat")
        scheduler = Scheduler(owner=owner, pet=pet)

        for raw in ["high", "medium", "low"]:
            scheduler.add_task(Task(raw.capitalize(), 10, parse_priority(raw)))

        scheduled, skipped = scheduler.generate_plan()
        # HIGH should be first
        assert scheduled[0].task.priority == Priority.HIGH
        assert skipped == []

    def test_sample_tasks_flow_through_scheduler(self):
        """Constants sample tasks can be loaded and scheduled without errors."""
        owner = Owner("Alex", available_minutes=840)
        pet = Pet("Buddy", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)

        for entry in SAMPLE_TASKS:
            scheduler.add_task(Task(**entry))

        scheduled, skipped = scheduler.generate_plan()
        total_scheduled = sum(st.task.duration_minutes for st in scheduled)
        assert total_scheduled <= owner.available_minutes
        assert len(scheduled) + len(skipped) == len(SAMPLE_TASKS)

    def test_plan_explainer_explains_all_scheduled_tasks(self):
        """PlanExplainer.explain_task works for every item Scheduler produces."""
        owner = Owner("Jordan", available_minutes=480)
        pet = Pet("Mochi", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.add_task(Task("Walk", 30, Priority.HIGH))
        scheduler.add_task(Task("Feed", 10, Priority.MEDIUM))
        scheduler.add_task(Task("Play", 20, Priority.LOW))

        scheduled, skipped = scheduler.generate_plan()
        explainer = PlanExplainer(scheduled, skipped, owner, pet)

        for st in scheduled:
            explanation = explainer.explain_task(st)
            assert st.task.title in explanation
            assert st.start_time in explanation
            assert st.end_time in explanation


# ── Owner ↔ Scheduler connection ─────────────────────────────────────────────

class TestOwnerSchedulerConnection:
    def test_scheduler_respects_owner_available_minutes(self):
        """Scheduler never schedules more minutes than Owner.available_minutes."""
        owner = Owner("Jordan", available_minutes=45)
        pet = Pet("Mochi", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.add_task(Task("Walk", 30, Priority.HIGH))
        scheduler.add_task(Task("Feed", 10, Priority.HIGH))
        scheduler.add_task(Task("Play", 20, Priority.MEDIUM))  # should be skipped

        scheduled, skipped = scheduler.generate_plan()
        total = sum(st.task.duration_minutes for st in scheduled)
        assert total <= owner.available_minutes

    def test_changing_owner_minutes_changes_schedule(self):
        """Two owners with different time get different schedule lengths."""
        pet = Pet("Mochi", "dog")

        tasks = [Task(f"Task{i}", 30, Priority.MEDIUM) for i in range(4)]

        scheduler_short = Scheduler(Owner("Short", available_minutes=60), pet)
        scheduler_long = Scheduler(Owner("Long", available_minutes=240), pet)
        for t in tasks:
            scheduler_short.add_task(Task(t.title, t.duration_minutes, t.priority))
            scheduler_long.add_task(Task(t.title, t.duration_minutes, t.priority))

        short_scheduled, _ = scheduler_short.generate_plan()
        long_scheduled, _ = scheduler_long.generate_plan()
        assert len(short_scheduled) < len(long_scheduled)


# ── Completed task exclusion ──────────────────────────────────────────────────

class TestCompletedTaskExclusion:
    def test_completed_tasks_do_not_appear_in_scheduled_or_skipped(self):
        owner = Owner("Jordan", available_minutes=480)
        pet = Pet("Mochi", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)

        done = Task("Old task", 30, Priority.HIGH)
        done.mark_complete()
        pending = Task("New task", 20, Priority.MEDIUM)

        scheduler.add_task(done)
        scheduler.add_task(pending)

        scheduled, skipped = scheduler.generate_plan()
        all_tasks = [s.task for s in scheduled] + skipped
        assert done not in all_tasks
        assert pending in all_tasks


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_single_task_exactly_fills_window(self):
        owner = Owner("Jordan", available_minutes=30)
        pet = Pet("Mochi", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.add_task(Task("Walk", 30, Priority.HIGH))
        scheduled, skipped = scheduler.generate_plan()
        assert len(scheduled) == 1
        assert skipped == []

    def test_task_one_minute_over_window_is_skipped(self):
        owner = Owner("Jordan", available_minutes=29)
        pet = Pet("Mochi", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.add_task(Task("Walk", 30, Priority.HIGH))
        scheduled, skipped = scheduler.generate_plan()
        assert scheduled == []
        assert len(skipped) == 1

    def test_plan_explainer_total_minutes_matches_scheduler_output(self):
        owner = Owner("Jordan", available_minutes=480)
        pet = Pet("Mochi", "dog")
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.add_task(Task("Walk", 30, Priority.HIGH))
        scheduler.add_task(Task("Feed", 15, Priority.MEDIUM))

        scheduled, skipped = scheduler.generate_plan()
        explainer = PlanExplainer(scheduled, skipped, owner, pet)

        expected_total = sum(st.task.duration_minutes for st in scheduled)
        assert explainer.total_minutes_scheduled == expected_total
