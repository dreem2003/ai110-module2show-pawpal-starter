"""Tests to verify sample task constants are well-formed."""
import pytest
from models.priority import Priority
from models.task import Task
from constants.sample_tasks import SAMPLE_TASKS


class TestSampleTasks:
    def test_sample_tasks_is_non_empty_list(self):
        assert isinstance(SAMPLE_TASKS, list)
        assert len(SAMPLE_TASKS) > 0

    def test_all_entries_are_dicts(self):
        for entry in SAMPLE_TASKS:
            assert isinstance(entry, dict)

    def test_all_entries_have_required_keys(self):
        required = {"title", "duration_minutes", "priority", "category"}
        for entry in SAMPLE_TASKS:
            assert required.issubset(entry.keys()), (
                f"Entry missing keys: {required - entry.keys()}"
            )

    def test_all_titles_are_non_empty_strings(self):
        for entry in SAMPLE_TASKS:
            assert isinstance(entry["title"], str)
            assert len(entry["title"].strip()) > 0

    def test_all_durations_are_positive_ints(self):
        for entry in SAMPLE_TASKS:
            assert isinstance(entry["duration_minutes"], int)
            assert entry["duration_minutes"] > 0

    def test_all_priorities_are_priority_enum(self):
        for entry in SAMPLE_TASKS:
            assert isinstance(entry["priority"], Priority)

    def test_all_categories_are_non_empty_strings(self):
        for entry in SAMPLE_TASKS:
            assert isinstance(entry["category"], str)
            assert len(entry["category"].strip()) > 0

    def test_entries_can_construct_task_objects(self):
        for entry in SAMPLE_TASKS:
            task = Task(**entry)
            assert isinstance(task, Task)
