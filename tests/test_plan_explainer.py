"""Unit tests for PlanExplainer service."""
import pytest
from models import Owner, Pet, Task, ScheduledTask, Priority
from services.plan_explainer import PlanExplainer


def make_owner(name="Jordan", minutes=480) -> Owner:
    return Owner(name=name, available_minutes=minutes)


def make_pet(name="Mochi", species="dog") -> Pet:
    return Pet(name=name, species=species, age=3)


def make_scheduled(title="Walk", duration=30, priority=Priority.HIGH,
                   start="08:00", end="08:30", reason="1st task") -> ScheduledTask:
    task = Task(title=title, duration_minutes=duration, priority=priority)
    return ScheduledTask(task=task, start_time=start, end_time=end, reason=reason)


# ── summarize ─────────────────────────────────────────────────────────────────

class TestSummarize:
    def test_includes_pet_name(self):
        explainer = PlanExplainer([make_scheduled()], [], make_owner(), make_pet("Mochi"))
        assert "Mochi" in explainer.summarize()

    def test_includes_owner_name(self):
        explainer = PlanExplainer([make_scheduled()], [], make_owner("Jordan"), make_pet())
        assert "Jordan" in explainer.summarize()

    def test_correct_scheduled_count(self):
        tasks = [make_scheduled("Walk"), make_scheduled("Feed", start="08:30", end="08:40")]
        explainer = PlanExplainer(tasks, [], make_owner(), make_pet())
        assert "2" in explainer.summarize()

    def test_correct_skipped_count(self):
        skipped = [Task("Bath", 60, Priority.LOW)]
        explainer = PlanExplainer([], skipped, make_owner(), make_pet())
        assert "1" in explainer.summarize()

    def test_total_minutes_correct(self):
        tasks = [
            make_scheduled("Walk", duration=30),
            make_scheduled("Feed", duration=10, start="08:30", end="08:40"),
        ]
        explainer = PlanExplainer(tasks, [], make_owner(), make_pet())
        assert "40" in explainer.summarize()

    def test_zero_tasks_summary(self):
        explainer = PlanExplainer([], [], make_owner(), make_pet())
        summary = explainer.summarize()
        assert "0" in summary


# ── explain_task ──────────────────────────────────────────────────────────────

class TestExplainTask:
    def test_includes_task_title(self):
        st = make_scheduled("Morning walk")
        explainer = PlanExplainer([st], [], make_owner(), make_pet())
        assert "Morning walk" in explainer.explain_task(st)

    def test_includes_start_and_end_time(self):
        st = make_scheduled(start="09:00", end="09:30")
        explainer = PlanExplainer([st], [], make_owner(), make_pet())
        result = explainer.explain_task(st)
        assert "09:00" in result
        assert "09:30" in result

    def test_includes_reason(self):
        st = make_scheduled(reason="High priority health task")
        explainer = PlanExplainer([st], [], make_owner(), make_pet())
        assert "High priority health task" in explainer.explain_task(st)


# ── explain_skipped ───────────────────────────────────────────────────────────

class TestExplainSkipped:
    def test_no_skipped_returns_all_fit_message(self):
        explainer = PlanExplainer([make_scheduled()], [], make_owner(), make_pet())
        assert "All tasks fit" in explainer.explain_skipped()

    def test_skipped_task_title_appears(self):
        skipped = [Task("Bath", 60, Priority.LOW)]
        explainer = PlanExplainer([], skipped, make_owner(), make_pet())
        assert "Bath" in explainer.explain_skipped()

    def test_multiple_skipped_titles_appear(self):
        skipped = [Task("Bath", 60, Priority.LOW), Task("Vet visit", 90, Priority.MEDIUM)]
        explainer = PlanExplainer([], skipped, make_owner(), make_pet())
        result = explainer.explain_skipped()
        assert "Bath" in result
        assert "Vet visit" in result

    def test_skipped_message_suggests_action(self):
        skipped = [Task("Bath", 60, Priority.LOW)]
        explainer = PlanExplainer([], skipped, make_owner(), make_pet())
        result = explainer.explain_skipped()
        # Should mention remediation hint
        assert "time" in result.lower() or "duration" in result.lower()
