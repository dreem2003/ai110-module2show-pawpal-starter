"""Unit tests for all model classes."""
import pytest
from models.priority import Priority
from models.task import Task, ScheduledTask
from models.pet import Pet
from models.owner import Owner


# ── Priority ──────────────────────────────────────────────────────────────────

class TestPriority:
    def test_values_are_ordered(self):
        assert Priority.LOW.value < Priority.MEDIUM.value < Priority.HIGH.value

    def test_enum_members_exist(self):
        assert Priority.LOW
        assert Priority.MEDIUM
        assert Priority.HIGH

    def test_by_name(self):
        assert Priority["HIGH"] == Priority.HIGH


# ── Task ──────────────────────────────────────────────────────────────────────

class TestTask:
    def test_creation_defaults(self):
        task = Task(title="Walk", duration_minutes=30, priority=Priority.HIGH)
        assert task.category == "general"
        assert task.completed is False

    def test_creation_explicit(self):
        task = Task("Grooming", 15, Priority.MEDIUM, category="grooming")
        assert task.title == "Grooming"
        assert task.duration_minutes == 15
        assert task.priority == Priority.MEDIUM
        assert task.category == "grooming"

    def test_mark_complete(self):
        task = Task("Walk", 30, Priority.HIGH)
        task.mark_complete()
        assert task.completed is True

    def test_mark_complete_idempotent(self):
        task = Task("Walk", 30, Priority.HIGH)
        task.mark_complete()
        task.mark_complete()
        assert task.completed is True

    def test_str_includes_priority_title_duration(self):
        task = Task("Walk", 30, Priority.HIGH)
        result = str(task)
        assert "HIGH" in result
        assert "Walk" in result
        assert "30" in result


# ── ScheduledTask ─────────────────────────────────────────────────────────────

class TestScheduledTask:
    def test_creation(self):
        task = Task("Walk", 30, Priority.HIGH)
        st = ScheduledTask(task=task, start_time="08:00", end_time="08:30")
        assert st.task is task
        assert st.start_time == "08:00"
        assert st.end_time == "08:30"
        assert st.reason == ""

    def test_creation_with_reason(self):
        task = Task("Walk", 30, Priority.HIGH)
        st = ScheduledTask(task, "08:00", "08:30", reason="First task")
        assert st.reason == "First task"


# ── Pet ───────────────────────────────────────────────────────────────────────

class TestPet:
    def test_creation_defaults(self):
        pet = Pet(name="Mochi", species="dog")
        assert pet.age == 0
        assert pet.notes == ""

    def test_creation_explicit(self):
        pet = Pet("Mochi", "dog", age=3, notes="Loves walks")
        assert pet.name == "Mochi"
        assert pet.species == "dog"
        assert pet.age == 3

    def test_str_includes_name_species_age(self):
        pet = Pet("Mochi", "dog", age=3)
        result = str(pet)
        assert "Mochi" in result
        assert "dog" in result
        assert "3" in result


# ── Owner ─────────────────────────────────────────────────────────────────────

class TestOwner:
    def test_creation_defaults(self):
        owner = Owner(name="Jordan")
        assert owner.available_minutes == 480
        assert owner.preferences == ""
        assert owner.pets == []

    def test_add_pet(self):
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog")
        owner.add_pet(pet)
        assert len(owner.pets) == 1
        assert owner.pets[0] is pet

    def test_add_multiple_pets(self):
        owner = Owner("Jordan")
        owner.add_pet(Pet("Mochi", "dog"))
        owner.add_pet(Pet("Luna", "cat"))
        assert len(owner.pets) == 2

    def test_str_includes_name_and_minutes(self):
        owner = Owner("Jordan", available_minutes=240)
        result = str(owner)
        assert "Jordan" in result
        assert "240" in result
