"""Unit tests for input validation utilities."""
import pytest
from models.priority import Priority
from utils.validators import (
    validate_duration,
    validate_available_minutes,
    validate_species,
    parse_priority,
)


# ── validate_duration ─────────────────────────────────────────────────────────

class TestValidateDuration:
    def test_valid_duration_returns_value(self):
        assert validate_duration(30) == 30

    def test_minimum_valid_duration(self):
        assert validate_duration(1) == 1

    def test_large_valid_duration(self):
        assert validate_duration(240) == 240

    def test_zero_raises(self):
        with pytest.raises(ValueError, match="at least 1"):
            validate_duration(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_duration(-5)


# ── validate_available_minutes ────────────────────────────────────────────────

class TestValidateAvailableMinutes:
    def test_valid_middle_value(self):
        assert validate_available_minutes(480) == 480

    def test_lower_boundary(self):
        assert validate_available_minutes(30) == 30

    def test_upper_boundary(self):
        assert validate_available_minutes(840) == 840

    def test_below_minimum_raises(self):
        with pytest.raises(ValueError, match="30"):
            validate_available_minutes(29)

    def test_above_maximum_raises(self):
        with pytest.raises(ValueError, match="840"):
            validate_available_minutes(841)

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            validate_available_minutes(0)


# ── validate_species ──────────────────────────────────────────────────────────

class TestValidateSpecies:
    @pytest.mark.parametrize("species", ["dog", "cat", "rabbit", "bird", "other"])
    def test_valid_species(self, species):
        assert validate_species(species) == species

    def test_normalises_uppercase(self):
        assert validate_species("DOG") == "dog"

    def test_normalises_mixed_case(self):
        assert validate_species("Cat") == "cat"

    def test_strips_whitespace(self):
        assert validate_species("  dog  ") == "dog"

    def test_invalid_species_raises(self):
        with pytest.raises(ValueError, match="Unknown species"):
            validate_species("dragon")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            validate_species("")


# ── parse_priority ────────────────────────────────────────────────────────────

class TestParsePriority:
    def test_low_returns_enum(self):
        assert parse_priority("low") == Priority.LOW

    def test_medium_returns_enum(self):
        assert parse_priority("medium") == Priority.MEDIUM

    def test_high_returns_enum(self):
        assert parse_priority("high") == Priority.HIGH

    def test_uppercase_input(self):
        assert parse_priority("HIGH") == Priority.HIGH

    def test_mixed_case_input(self):
        assert parse_priority("Medium") == Priority.MEDIUM

    def test_strips_whitespace(self):
        assert parse_priority("  low  ") == Priority.LOW

    def test_invalid_priority_raises(self):
        with pytest.raises(ValueError, match="Unknown priority"):
            parse_priority("urgent")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_priority("")
