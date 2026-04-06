"""Unit tests for Scheduler service."""
import pytest
from models import Owner, Pet, Task, ScheduledTask, Priority
from services.scheduler import Scheduler


def make_owner(minutes: int = 480) -> Owner:
    return Owner(name="Jordan", available_minutes=minutes)


def make_pet() -> Pet:
    return Pet(name="Mochi", species="dog", age=3)


def make_task(title="Walk", duration=30, priority=Priority.HIGH, category="exercise") -> Task:
    return Task(title=title, duration_minutes=duration, priority=priority, category=category)


# ── Task management ───────────────────────────────────────────────────────────

class TestTaskManagement:
    def test_add_task(self):
        scheduler = Scheduler(make_owner(), make_pet())
        task = make_task()
        scheduler.add_task(task)
        assert task in scheduler.tasks

    def test_add_multiple_tasks(self):
        scheduler = Scheduler(make_owner(), make_pet())
        t1, t2 = make_task("Walk"), make_task("Feed", 10, Priority.HIGH)
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        assert len(scheduler.tasks) == 2

    def test_remove_task_by_title(self):
        scheduler = Scheduler(make_owner(), make_pet())
        task = make_task("Walk")
        scheduler.add_task(task)
        scheduler.remove_task("Walk")
        assert task not in scheduler.tasks

    def test_remove_nonexistent_task_is_safe(self):
        scheduler = Scheduler(make_owner(), make_pet())
        scheduler.add_task(make_task("Walk"))
        scheduler.remove_task("Ghost task")
        assert len(scheduler.tasks) == 1

    def test_remove_task_only_matching_title(self):
        scheduler = Scheduler(make_owner(), make_pet())
        t1 = make_task("Walk")
        t2 = make_task("Feed")
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        scheduler.remove_task("Walk")
        assert t2 in scheduler.tasks
        assert t1 not in scheduler.tasks


# ── generate_plan ─────────────────────────────────────────────────────────────

class TestGeneratePlan:
    def test_empty_tasks_returns_empty_lists(self):
        scheduler = Scheduler(make_owner(), make_pet())
        scheduled, skipped = scheduler.generate_plan()
        assert scheduled == []
        assert skipped == []

    def test_single_task_is_scheduled(self):
        scheduler = Scheduler(make_owner(480), make_pet())
        scheduler.add_task(make_task("Walk", 30, Priority.HIGH))
        scheduled, skipped = scheduler.generate_plan()
        assert len(scheduled) == 1
        assert skipped == []

    def test_high_priority_scheduled_before_low(self):
        scheduler = Scheduler(make_owner(480), make_pet())
        scheduler.add_task(make_task("Low task", 20, Priority.LOW))
        scheduler.add_task(make_task("High task", 20, Priority.HIGH))
        scheduled, _ = scheduler.generate_plan()
        assert scheduled[0].task.title == "High task"
        assert scheduled[1].task.title == "Low task"

    def test_all_three_priorities_ordered(self):
        scheduler = Scheduler(make_owner(480), make_pet())
        scheduler.add_task(make_task("Low", 10, Priority.LOW))
        scheduler.add_task(make_task("High", 10, Priority.HIGH))
        scheduler.add_task(make_task("Medium", 10, Priority.MEDIUM))
        scheduled, _ = scheduler.generate_plan()
        priorities = [s.task.priority for s in scheduled]
        assert priorities == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]

    def test_task_exceeding_available_minutes_is_skipped(self):
        scheduler = Scheduler(make_owner(minutes=20), make_pet())
        scheduler.add_task(make_task("Long walk", 60, Priority.HIGH))
        scheduled, skipped = scheduler.generate_plan()
        assert scheduled == []
        assert len(skipped) == 1
        assert skipped[0].title == "Long walk"

    def test_partial_fit_schedules_what_fits(self):
        scheduler = Scheduler(make_owner(minutes=40), make_pet())
        scheduler.add_task(make_task("Walk", 30, Priority.HIGH))
        scheduler.add_task(make_task("Bath", 60, Priority.MEDIUM))
        scheduled, skipped = scheduler.generate_plan()
        assert len(scheduled) == 1
        assert scheduled[0].task.title == "Walk"
        assert len(skipped) == 1
        assert skipped[0].title == "Bath"

    def test_completed_tasks_are_excluded(self):
        scheduler = Scheduler(make_owner(480), make_pet())
        task = make_task("Walk", 30, Priority.HIGH)
        task.mark_complete()
        scheduler.add_task(task)
        scheduled, skipped = scheduler.generate_plan()
        assert scheduled == []
        assert skipped == []

    def test_time_slots_are_sequential(self):
        scheduler = Scheduler(make_owner(480), make_pet(), day_start_minute=480)
        scheduler.add_task(make_task("Walk", 30, Priority.HIGH))
        scheduler.add_task(make_task("Feed", 10, Priority.MEDIUM))
        scheduled, _ = scheduler.generate_plan()
        assert scheduled[0].start_time == "08:00"
        assert scheduled[0].end_time == "08:30"
        assert scheduled[1].start_time == "08:30"
        assert scheduled[1].end_time == "08:40"

    def test_available_minutes_caps_window(self):
        # Owner has only 30 min even though day window is 14 hours
        scheduler = Scheduler(make_owner(minutes=30), make_pet())
        scheduler.add_task(make_task("Walk", 20, Priority.HIGH))
        scheduler.add_task(make_task("Feed", 20, Priority.MEDIUM))
        scheduled, skipped = scheduler.generate_plan()
        assert len(scheduled) == 1
        assert len(skipped) == 1

    def test_returned_scheduled_tasks_are_scheduled_task_instances(self):
        scheduler = Scheduler(make_owner(), make_pet())
        scheduler.add_task(make_task())
        scheduled, _ = scheduler.generate_plan()
        assert isinstance(scheduled[0], ScheduledTask)

    def test_reason_is_populated(self):
        scheduler = Scheduler(make_owner(), make_pet())
        scheduler.add_task(make_task())
        scheduled, _ = scheduler.generate_plan()
        assert scheduled[0].reason != ""
