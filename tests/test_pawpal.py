import pytest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add parent directory to path to import pawpal_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import (
    Pet, Task, Owner, Scheduler, ScheduledTask, Schedule, SchedulingConstraints,
    Priority, TaskCategory, TaskStatus, EnergyLevel, TimeOfDay, 
    ActivityPreference, MedicalCondition
)


class TestTaskCompletion:
    """Test task completion functionality"""
    
    def test_mark_completed_changes_last_completed(self):
        """Verify that calling mark_completed() sets the last_completed timestamp."""
        # Arrange
        task = Task("Feed Pet", 10, Priority.HIGH, TaskCategory.FEEDING)
        
        # Verify last_completed is initially None
        assert task.last_completed is None
        
        # Act
        before_completion = datetime.now()
        task.mark_completed()
        after_completion = datetime.now()
        
        # Assert
        assert task.last_completed is not None
        assert before_completion <= task.last_completed <= after_completion
    
    def test_scheduled_task_status_changes(self):
        """Verify that ScheduledTask status can be changed and affects underlying task."""
        # Arrange
        task = Task("Walk Dog", 30, Priority.MEDIUM, TaskCategory.EXERCISE)
        scheduled_task = ScheduledTask(
            task=task, 
            scheduled_time=datetime.now(),
            reason="High priority task"
        )
        
        # Verify initial status is PENDING
        assert scheduled_task.get_status() == TaskStatus.PENDING
        assert task.last_completed is None
        
        # Act
        before_completion = datetime.now()
        scheduled_task.set_status(TaskStatus.COMPLETED)
        after_completion = datetime.now()
        
        # Assert
        assert scheduled_task.get_status() == TaskStatus.COMPLETED
        assert task.last_completed is not None
        assert before_completion <= task.last_completed <= after_completion


class TestTaskAddition:
    """Test task addition to pets functionality"""
    
    def test_adding_task_increases_scheduler_task_count(self):
        """Verify that adding a task to the Scheduler increases the available task count."""
        # Arrange
        pet = Pet("Buddy", "dog", 3, "Golden Retriever")
        owner = Owner("Alex", 240)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        # Get initial task count
        initial_task_count = len(scheduler.available_tasks)
        
        # Create a task
        task = Task("Brush Pet", 15, Priority.LOW, TaskCategory.GROOMING)
        task.add_species_requirement("dog")
        
        # Act
        scheduler.add_task(task)
        
        # Assert
        final_task_count = len(scheduler.available_tasks)
        assert final_task_count == initial_task_count + 1
    
    def test_multiple_tasks_increase_count_correctly(self):
        """Verify that adding multiple tasks correctly increases the count."""
        # Arrange
        pet = Pet("Luna", "cat", 5, "Persian")
        owner = Owner("Sarah", 180)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        # Create multiple tasks
        tasks = [
            Task("Feed Cat", 5, Priority.CRITICAL, TaskCategory.FEEDING),
            Task("Clean Litter Box", 10, Priority.MEDIUM, TaskCategory.MAINTENANCE),
            Task("Play with Cat", 20, Priority.LOW, TaskCategory.ENRICHMENT)
        ]
        
        # Add species requirements
        for task in tasks:
            task.add_species_requirement("cat")
        
        initial_count = len(scheduler.available_tasks)
        
        # Act
        for task in tasks:
            scheduler.add_task(task)
        
        # Assert
        final_count = len(scheduler.available_tasks)
        assert final_count == initial_count + len(tasks)
    
    def test_task_applicable_to_correct_pet(self):
        """Verify that tasks are correctly associated with appropriate pets."""
        # Arrange
        dog = Pet("Rex", "dog", 2, "Border Collie")
        cat = Pet("Whiskers", "cat", 4, "Siamese")
        owner = Owner("Tom", 300)
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        # Create species-specific tasks
        dog_task = Task("Dog Walk", 45, Priority.HIGH, TaskCategory.EXERCISE)
        dog_task.add_species_requirement("dog")
        
        cat_task = Task("Cat Grooming", 20, Priority.MEDIUM, TaskCategory.GROOMING)
        cat_task.add_species_requirement("cat")
        
        # Act & Assert
        assert dog_task.is_applicable_for_pet(dog) == True
        assert dog_task.is_applicable_for_pet(cat) == False
        
        assert cat_task.is_applicable_for_pet(cat) == True
        assert cat_task.is_applicable_for_pet(dog) == False


class TestTaskFiltering:
    """Test energy level and medical condition filtering"""
    
    def test_energy_level_filtering(self):
        """Verify that tasks respect pet energy levels."""
        # Arrange
        high_energy_dog = Pet("Bolt", "dog", 1, "Jack Russell")
        high_energy_dog.set_energy_level(EnergyLevel.VERY_HIGH)
        
        low_energy_cat = Pet("Sleepy", "cat", 12, "Persian")
        low_energy_cat.set_energy_level(EnergyLevel.LOW)
        
        # Create energy-specific task
        intensive_task = Task("Agility Training", 60, Priority.MEDIUM, TaskCategory.TRAINING)
        intensive_task.add_species_requirement("dog")
        intensive_task.add_energy_requirement(EnergyLevel.HIGH)
        
        gentle_task = Task("Gentle Brushing", 15, Priority.LOW, TaskCategory.GROOMING)
        gentle_task.add_species_requirement("cat")
        gentle_task.add_energy_requirement(EnergyLevel.LOW)
        
        # Act & Assert
        assert intensive_task.is_applicable_for_pet(high_energy_dog) == True
        assert gentle_task.is_applicable_for_pet(low_energy_cat) == True


# ============================================================================
# COMPREHENSIVE TEST SUITE WITH EDGE CASES
# ============================================================================

class TestPetDataModel:
    """Test Pet class functionality including edge cases."""
    
    def test_pet_creation_basic(self):
        """Test basic pet creation with required fields."""
        pet = Pet("Buddy", "dog", 3)
        assert pet.name == "Buddy"
        assert pet.species == "dog"
        assert pet.age == 3
        assert pet.breed == ""
        assert pet.preferences == {}
        assert pet.medical_conditions == {}
    
    def test_pet_creation_with_all_fields(self):
        """Test pet creation with all optional fields."""
        preferences = {"walk_time": "morning"}
        conditions = {"arthritis": "mild"}
        pet = Pet("Luna", "cat", 5, "Persian", preferences, conditions)
        
        assert pet.name == "Luna"
        assert pet.species == "cat"
        assert pet.age == 5
        assert pet.breed == "Persian"
        assert pet.preferences == preferences
        assert pet.medical_conditions == conditions
    
    def test_pet_age_edge_cases(self):
        """Test pet creation with edge case ages."""
        # Very young pet
        young_pet = Pet("Puppy", "dog", 0)
        assert young_pet.age == 0
        
        # Very old pet
        old_pet = Pet("Senior", "cat", 25)
        assert old_pet.age == 25
        
        # Negative age (currently allowed by implementation)
        negative_age_pet = Pet("Invalid", "dog", -1)
        assert negative_age_pet.age == -1
    
    def test_add_preference(self):
        """Test adding preferences to pet."""
        pet = Pet("Max", "dog", 4)
        pet.add_preference("walk_time", "morning")
        pet.add_preference("food_type", "kibble")
        
        assert pet.preferences["walk_time"] == "morning"
        assert pet.preferences["food_type"] == "kibble"
        assert len(pet.preferences) == 2
    
    def test_set_time_preference_with_enum(self):
        """Test setting time preferences using TimeOfDay enum."""
        pet = Pet("Whiskers", "cat", 2)
        pet.set_time_preference("grooming", TimeOfDay.AFTERNOON)
        
        assert pet.preferences["grooming_time"] == "afternoon"
    
    def test_set_energy_level(self):
        """Test setting energy levels."""
        pet = Pet("Flash", "dog", 1)
        pet.set_energy_level(EnergyLevel.VERY_HIGH)
        
        assert pet.preferences["energy_level"] == "very_high"
    
    def test_set_activity_preference(self):
        """Test setting activity preferences."""
        pet = Pet("Indoor", "cat", 8)
        pet.set_activity_preference(ActivityPreference.INDOOR_ONLY)
        
        assert pet.preferences["activity_style"] == "indoor_only"
    
    def test_get_preferences_returns_copy(self):
        """Test that get_preferences returns a copy, not reference."""
        pet = Pet("Test", "dog", 3)
        pet.add_preference("test", "value")
        
        prefs = pet.get_preferences()
        prefs["new_key"] = "new_value"
        
        assert "new_key" not in pet.preferences
        assert pet.get_preferences() == {"test": "value"}
    
    def test_add_medical_condition(self):
        """Test adding medical conditions."""
        pet = Pet("Sick", "dog", 10)
        pet.add_medical_condition(MedicalCondition.ARTHRITIS, "severe")
        pet.add_medical_condition(MedicalCondition.DIABETES)
        
        assert pet.medical_conditions["arthritis"] == "severe"
        assert pet.medical_conditions["diabetes"] == ""
    
    def test_has_medical_condition(self):
        """Test checking for medical conditions."""
        pet = Pet("Patient", "cat", 7)
        pet.add_medical_condition(MedicalCondition.HEART_CONDITION, "mild murmur")
        
        assert pet.has_medical_condition(MedicalCondition.HEART_CONDITION)
        assert not pet.has_medical_condition(MedicalCondition.ARTHRITIS)
    
    def test_get_medical_conditions_returns_copy(self):
        """Test that get_medical_conditions returns a copy."""
        pet = Pet("Test", "dog", 5)
        pet.add_medical_condition(MedicalCondition.ANXIETY, "separation anxiety")
        
        conditions = pet.get_medical_conditions()
        conditions["fake_condition"] = "fake_note"
        
        assert "fake_condition" not in pet.medical_conditions
    
    def test_pet_string_representation(self):
        """Test pet string representation."""
        pet = Pet("Buddy", "dog", 3, "Golden Retriever")
        expected = "Buddy (dog, Golden Retriever, 3 years old)"
        assert str(pet) == expected
    
    def test_empty_string_fields(self):
        """Test handling of empty string fields."""
        pet = Pet("", "", 0, "")
        assert pet.name == ""
        assert pet.species == ""
        assert pet.breed == ""
    
    def test_special_characters_in_name(self):
        """Test names with special characters."""
        pet = Pet("Mr. Fluff-a-lot!", "cat", 4)
        assert pet.name == "Mr. Fluff-a-lot!"


class TestOwnerDataModel:
    """Test Owner class functionality including edge cases."""
    
    def test_owner_creation_basic(self):
        """Test basic owner creation."""
        owner = Owner("John")
        assert owner.name == "John"
        assert owner.available_time_minutes == 120
        assert owner.time_windows == {}
        assert owner.preferences == {}
        assert owner.pets == []
    
    def test_owner_creation_with_time(self):
        """Test owner creation with custom available time."""
        owner = Owner("Jane", 480)
        assert owner.available_time_minutes == 480
    
    def test_add_pet(self):
        """Test adding pets to owner."""
        owner = Owner("Bob")
        pet1 = Pet("Dog1", "dog", 3)
        pet2 = Pet("Cat1", "cat", 5)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        assert len(owner.pets) == 2
        assert pet1 in owner.pets
        assert pet2 in owner.pets
    
    def test_add_duplicate_pet(self):
        """Test adding same pet multiple times."""
        owner = Owner("Alice")
        pet = Pet("Duplicate", "dog", 2)
        
        owner.add_pet(pet)
        owner.add_pet(pet)  # Should not add duplicate
        
        assert len(owner.pets) == 1
        assert pet in owner.pets
    
    def test_remove_pet(self):
        """Test removing pets from owner."""
        owner = Owner("Charlie")
        pet1 = Pet("Keep", "dog", 4)
        pet2 = Pet("Remove", "cat", 6)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        owner.remove_pet(pet2)
        
        assert len(owner.pets) == 1
        assert pet1 in owner.pets
        assert pet2 not in owner.pets
    
    def test_remove_nonexistent_pet(self):
        """Test removing pet that doesn't belong to owner."""
        owner = Owner("Dave")
        pet = Pet("NotMine", "bird", 1)
        
        # Should not raise error
        owner.remove_pet(pet)
        assert len(owner.pets) == 0
    
    def test_get_pets_returns_copy(self):
        """Test that get_pets returns a copy."""
        owner = Owner("Eve")
        pet = Pet("Original", "dog", 3)
        owner.add_pet(pet)
        
        pets_copy = owner.get_pets()
        fake_pet = Pet("Fake", "cat", 1)
        pets_copy.append(fake_pet)
        
        assert len(owner.pets) == 1
        assert fake_pet not in owner.pets
    
    def test_set_time_window(self):
        """Test setting time windows."""
        owner = Owner("Frank")
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        
        owner.set_time_window(start, end)
        
        assert "default" in owner.time_windows
        assert owner.time_windows["default"]["start"] == start
        assert owner.time_windows["default"]["end"] == end
        assert owner.available_time_minutes == 600  # 10 hours
    
    def test_set_time_window_edge_cases(self):
        """Test time window edge cases."""
        owner = Owner("Grace")
        
        # Same start and end time
        start = end = datetime(2024, 1, 1, 12, 0)
        owner.set_time_window(start, end)
        assert owner.available_time_minutes == 0
        
        # End before start (negative duration)
        start = datetime(2024, 1, 1, 18, 0)
        end = datetime(2024, 1, 1, 8, 0)
        owner.set_time_window(start, end)
        # Should handle gracefully (negative time)
        assert owner.available_time_minutes < 0
    
    def test_get_available_time(self):
        """Test getting available time."""
        owner = Owner("Henry", 300)
        assert owner.get_available_time() == 300
    
    def test_add_preference(self):
        """Test adding owner preferences."""
        owner = Owner("Iris")
        owner.add_preference("morning_person", "true")
        owner.add_preference("preferred_duration", "short")
        
        assert owner.preferences["morning_person"] == "true"
        assert owner.preferences["preferred_duration"] == "short"
    
    def test_get_preferences_returns_copy(self):
        """Test that get_preferences returns a copy."""
        owner = Owner("Jack")
        owner.add_preference("test", "value")
        
        prefs = owner.get_preferences()
        prefs["fake"] = "fake_value"
        
        assert "fake" not in owner.preferences
    
    def test_owner_string_representation(self):
        """Test owner string representation."""
        owner = Owner("Kate")
        pet1 = Pet("Pet1", "dog", 2)
        pet2 = Pet("Pet2", "cat", 4)
        
        # No pets
        assert str(owner) == "Kate (0 pets)"
        
        # One pet
        owner.add_pet(pet1)
        assert str(owner) == "Kate (1 pet)"
        
        # Multiple pets
        owner.add_pet(pet2)
        assert str(owner) == "Kate (2 pets)"


class TestTaskDataModel:
    """Test Task class functionality including edge cases."""
    
    def test_task_creation_basic(self):
        """Test basic task creation."""
        task = Task("Feed Pet", 10)
        assert task.title == "Feed Pet"
        assert task.duration_minutes == 10
        assert task.priority == Priority.MEDIUM
        assert task.category == TaskCategory.GENERAL
        assert not task.is_recurring
        assert task.frequency_days == 0
        assert task.requirements == {}
        assert task.last_completed is None
    
    def test_task_creation_with_all_params(self):
        """Test task creation with all parameters."""
        task = Task(
            "Walk Dog",
            30,
            Priority.HIGH,
            TaskCategory.EXERCISE,
            True,
            1,
            {"species": "dog"}
        )
        assert task.title == "Walk Dog"
        assert task.duration_minutes == 30
        assert task.priority == Priority.HIGH
        assert task.category == TaskCategory.EXERCISE
        assert task.is_recurring
        assert task.frequency_days == 1
        assert task.requirements == {"species": "dog"}
    
    def test_set_recurring(self):
        """Test setting task as recurring."""
        task = Task("Daily Feed", 5)
        task.set_recurring(1)
        
        assert task.is_recurring
        assert task.frequency_days == 1
    
    def test_add_species_requirement(self):
        """Test adding species requirements."""
        task = Task("Dog Walk", 30)
        task.add_species_requirement("Dog")  # Test case insensitive
        
        assert task.requirements["species"] == "dog"
    
    def test_add_medical_restriction(self):
        """Test adding medical restrictions."""
        task = Task("High Impact Exercise", 45)
        task.add_medical_restriction(MedicalCondition.ARTHRITIS)
        task.add_medical_restriction(MedicalCondition.HIP_DYSPLASIA)
        
        restrictions = task.requirements["medical_restrictions"]
        assert "arthritis" in restrictions
        assert "hip_dysplasia" in restrictions
        assert len(restrictions) == 2
    
    def test_add_energy_requirement(self):
        """Test adding energy requirements."""
        task = Task("Intense Training", 60)
        task.add_energy_requirement(EnergyLevel.HIGH)
        
        assert task.requirements["min_energy_level"] == "high"
    
    def test_is_applicable_for_pet_species_mismatch(self):
        """Test task applicability with species mismatch."""
        dog = Pet("Buddy", "dog", 3)
        cat = Pet("Whiskers", "cat", 5)
        
        dog_task = Task("Dog Walk", 30)
        dog_task.add_species_requirement("dog")
        
        assert dog_task.is_applicable_for_pet(dog)
        assert not dog_task.is_applicable_for_pet(cat)
    
    def test_is_applicable_for_pet_medical_restriction(self):
        """Test task applicability with medical restrictions."""
        sick_pet = Pet("Sick", "dog", 8)
        sick_pet.add_medical_condition(MedicalCondition.ARTHRITIS)
        
        healthy_pet = Pet("Healthy", "dog", 3)
        
        intensive_task = Task("High Impact", 45)
        intensive_task.add_medical_restriction(MedicalCondition.ARTHRITIS)
        
        assert not intensive_task.is_applicable_for_pet(sick_pet)
        assert intensive_task.is_applicable_for_pet(healthy_pet)
    
    def test_is_applicable_for_pet_energy_requirement(self):
        """Test task applicability with energy requirements."""
        high_energy_pet = Pet("Energetic", "dog", 2)
        high_energy_pet.set_energy_level(EnergyLevel.VERY_HIGH)
        
        low_energy_pet = Pet("Lazy", "cat", 10)
        low_energy_pet.set_energy_level(EnergyLevel.LOW)
        
        demanding_task = Task("Marathon Walk", 120)
        demanding_task.add_energy_requirement(EnergyLevel.HIGH)
        
        assert demanding_task.is_applicable_for_pet(high_energy_pet)
        assert not demanding_task.is_applicable_for_pet(low_energy_pet)
    
    def test_is_applicable_complex_requirements(self):
        """Test task applicability with multiple requirements."""
        pet = Pet("Complex", "dog", 5)
        pet.set_energy_level(EnergyLevel.MODERATE)
        pet.add_medical_condition(MedicalCondition.DIABETES)
        
        # Task that matches species and energy but conflicts with medical condition
        complex_task = Task("Complex Task", 30)
        complex_task.add_species_requirement("dog")
        complex_task.add_energy_requirement(EnergyLevel.LOW)  # Pet has moderate, should pass
        complex_task.add_medical_restriction(MedicalCondition.DIABETES)  # Pet has diabetes, should fail
        
        assert not complex_task.is_applicable_for_pet(pet)
    
    def test_get_priority_score(self):
        """Test priority scoring."""
        task_low = Task("Low", 10, Priority.LOW)
        task_medium = Task("Medium", 10, Priority.MEDIUM)
        task_high = Task("High", 10, Priority.HIGH)
        task_critical = Task("Critical", 10, Priority.CRITICAL)
        
        assert task_low.get_priority_score() == 1
        assert task_medium.get_priority_score() == 2
        assert task_high.get_priority_score() == 3
        assert task_critical.get_priority_score() == 4
    
    def test_get_priority_score_overdue_bonus(self):
        """Test priority scoring with overdue bonus."""
        task = Task("Overdue", 10, Priority.LOW)
        task.set_recurring(1)
        task.last_completed = datetime.now() - timedelta(days=2)  # Overdue by 1 day
        
        score = task.get_priority_score()
        assert score == 3  # 1 (LOW priority) + 2 (overdue bonus)
    
    def test_is_overdue_not_recurring(self):
        """Test overdue check for non-recurring tasks."""
        task = Task("One-time", 10)
        assert not task.is_overdue()
    
    def test_is_overdue_no_completion(self):
        """Test overdue check with no completion history."""
        task = Task("Never Done", 10)
        task.set_recurring(1)
        assert not task.is_overdue()  # Can't be overdue if never completed
    
    def test_is_overdue_not_due_yet(self):
        """Test overdue check when not due yet."""
        task = Task("Recent", 10)
        task.set_recurring(2)
        task.last_completed = datetime.now() - timedelta(days=1)  # Only 1 day ago, frequency is 2
        
        assert not task.is_overdue()
    
    def test_is_overdue_exactly_due(self):
        """Test overdue check when exactly due."""
        task = Task("Due Now", 10)
        task.set_recurring(1)
        task.last_completed = datetime.now() - timedelta(days=1)  # Exactly 1 day ago
        
        assert task.is_overdue()
    
    def test_is_overdue_past_due(self):
        """Test overdue check when past due."""
        task = Task("Past Due", 10)
        task.set_recurring(1)
        task.last_completed = datetime.now() - timedelta(days=3)  # 3 days ago, frequency is 1
        
        assert task.is_overdue()
    
    def test_mark_completed_updates_timestamp(self):
        """Test that mark_completed updates the timestamp."""
        task = Task("Test Task", 10)
        
        before = datetime.now()
        task.mark_completed()
        after = datetime.now()
        
        assert task.last_completed is not None
        assert before <= task.last_completed <= after
    
    def test_mark_completed_recurring_task(self):
        """Test mark_completed behavior with recurring tasks."""
        task = Task("Daily Task", 15)
        task.set_recurring(1)
        
        # Mock the _create_next_recurring_instance method to verify it's called
        original_method = task._create_next_recurring_instance
        task._create_next_recurring_instance = MagicMock(return_value=Task("Next Instance", 15))
        
        task.mark_completed()
        
        assert task.last_completed is not None
        task._create_next_recurring_instance.assert_called_once()
        
        # Restore original method
        task._create_next_recurring_instance = original_method
    
    def test_create_next_recurring_instance(self):
        """Test creation of next recurring task instance."""
        original = Task("Original", 20, Priority.HIGH, TaskCategory.FEEDING)
        original.add_species_requirement("dog")
        original.set_recurring(7)  # Weekly
        original.last_completed = datetime.now()
        
        next_task = original._create_next_recurring_instance()
        
        assert next_task.title == "Original"
        assert next_task.duration_minutes == 20
        assert next_task.priority == Priority.HIGH
        assert next_task.category == TaskCategory.FEEDING
        assert next_task.requirements == original.requirements
        assert next_task.is_recurring
        assert next_task.frequency_days == 7
        assert next_task.last_completed is None  # Should be reset
    
    def test_task_string_representation(self):
        """Test task string representation."""
        task = Task("Test Task", 25, Priority.HIGH)
        expected = "Test Task (25 min, HIGH)"
        assert str(task) == expected
    
    def test_zero_duration_task(self):
        """Test task with zero duration."""
        task = Task("Instant", 0)
        assert task.duration_minutes == 0
    
    def test_negative_duration_task(self):
        """Test task with negative duration (currently allowed by implementation)."""
        task = Task("Invalid", -5)
        assert task.duration_minutes == -5
    
    def test_very_long_duration_task(self):
        """Test task with very long duration."""
        task = Task("All Day", 1440)  # 24 hours
        assert task.duration_minutes == 1440
    
    def test_empty_title_task(self):
        """Test task with empty title."""
        task = Task("", 10)
        assert task.title == ""


class TestScheduledTaskDataModel:
    """Test ScheduledTask class functionality including edge cases."""
    
    def test_scheduled_task_creation(self):
        """Test basic scheduled task creation."""
        task = Task("Test", 30)
        time = datetime(2024, 1, 1, 10, 0)
        reason = "High priority"
        
        scheduled = ScheduledTask(task, time, reason)
        
        assert scheduled.task == task
        assert scheduled.scheduled_time == time
        assert scheduled.reason == reason
        assert scheduled.duration_minutes == 30
        assert scheduled.status == TaskStatus.PENDING
    
    def test_scheduled_task_post_init(self):
        """Test that duration is correctly copied from task."""
        task = Task("Test", 45)
        scheduled = ScheduledTask(task, datetime.now())
        
        assert scheduled.duration_minutes == 45
    
    def test_get_task(self):
        """Test getting underlying task."""
        task = Task("Original", 20)
        scheduled = ScheduledTask(task, datetime.now())
        
        assert scheduled.get_task() == task
    
    def test_get_scheduled_time(self):
        """Test getting scheduled time."""
        time = datetime(2024, 1, 1, 14, 30)
        scheduled = ScheduledTask(Task("Test", 10), time)
        
        assert scheduled.get_scheduled_time() == time
    
    def test_get_end_time(self):
        """Test calculating end time."""
        start = datetime(2024, 1, 1, 9, 0)
        task = Task("Test", 45)
        scheduled = ScheduledTask(task, start)
        
        expected_end = datetime(2024, 1, 1, 9, 45)
        assert scheduled.get_end_time() == expected_end
    
    def test_set_status(self):
        """Test setting task status."""
        scheduled = ScheduledTask(Task("Test", 10), datetime.now())
        
        scheduled.set_status(TaskStatus.IN_PROGRESS)
        assert scheduled.status == TaskStatus.IN_PROGRESS
        
        scheduled.set_status(TaskStatus.SKIPPED)
        assert scheduled.status == TaskStatus.SKIPPED
    
    def test_set_status_completed_marks_underlying_task(self):
        """Test that setting COMPLETED status marks underlying task."""
        task = Task("Test", 15)
        scheduled = ScheduledTask(task, datetime.now())
        
        assert task.last_completed is None
        
        scheduled.set_status(TaskStatus.COMPLETED)
        
        assert scheduled.status == TaskStatus.COMPLETED
        assert task.last_completed is not None
    
    def test_get_next_recurring_task_non_recurring(self):
        """Test getting next recurring task for non-recurring task."""
        task = Task("One-time", 10)
        scheduled = ScheduledTask(task, datetime.now())
        scheduled.set_status(TaskStatus.COMPLETED)
        
        assert scheduled.get_next_recurring_task() is None
    
    def test_get_next_recurring_task_not_completed(self):
        """Test getting next recurring task when not completed."""
        task = Task("Recurring", 10)
        task.set_recurring(1)
        scheduled = ScheduledTask(task, datetime.now())
        
        assert scheduled.get_next_recurring_task() is None
    
    def test_get_next_recurring_task_completed_recurring(self):
        """Test getting next recurring task when completed."""
        task = Task("Daily", 20)
        task.set_recurring(1)
        scheduled = ScheduledTask(task, datetime.now())
        scheduled.set_status(TaskStatus.COMPLETED)
        
        next_task = scheduled.get_next_recurring_task()
        
        assert next_task is not None
        assert next_task.title == "Daily"
        assert next_task.duration_minutes == 20
        assert next_task.is_recurring
        assert next_task.frequency_days == 1
    
    def test_get_status(self):
        """Test getting task status."""
        scheduled = ScheduledTask(Task("Test", 10), datetime.now())
        assert scheduled.get_status() == TaskStatus.PENDING
    
    def test_get_reason(self):
        """Test getting scheduling reason."""
        reason = "Pet's preferred time"
        scheduled = ScheduledTask(Task("Test", 10), datetime.now(), reason)
        assert scheduled.get_reason() == reason
    
    def test_scheduled_task_string_representation(self):
        """Test scheduled task string representation."""
        task = Task("Morning Walk", 30)
        time = datetime(2024, 1, 1, 8, 0)
        scheduled = ScheduledTask(task, time)
        
        expected = "08:00 AM - Morning Walk (30 min)"
        assert str(scheduled) == expected
    
    def test_zero_duration_scheduled_task(self):
        """Test scheduled task with zero duration."""
        task = Task("Instant", 0)
        time = datetime(2024, 1, 1, 12, 0)
        scheduled = ScheduledTask(task, time)
        
        assert scheduled.get_end_time() == time  # Same as start time


class TestScheduleDataModel:
    """Test Schedule class functionality including edge cases."""
    
    def test_schedule_creation(self):
        """Test basic schedule creation."""
        date = datetime(2024, 1, 1)
        schedule = Schedule(date)
        
        assert schedule.date == date
        assert schedule.scheduled_tasks == []
        assert schedule.total_duration_minutes == 0
        assert schedule.metadata == {}
    
    def test_add_scheduled_task(self):
        """Test adding scheduled tasks."""
        schedule = Schedule(datetime(2024, 1, 1))
        task = Task("Test", 30)
        scheduled = ScheduledTask(task, datetime(2024, 1, 1, 10, 0))
        
        schedule.add_scheduled_task(scheduled)
        
        assert len(schedule.scheduled_tasks) == 1
        assert scheduled in schedule.scheduled_tasks
        assert schedule.total_duration_minutes == 30
    
    def test_add_multiple_scheduled_tasks(self):
        """Test adding multiple scheduled tasks."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        tasks = [
            ScheduledTask(Task("Task1", 15), datetime(2024, 1, 1, 9, 0)),
            ScheduledTask(Task("Task2", 25), datetime(2024, 1, 1, 10, 0)),
            ScheduledTask(Task("Task3", 10), datetime(2024, 1, 1, 11, 0))
        ]
        
        for scheduled_task in tasks:
            schedule.add_scheduled_task(scheduled_task)
        
        assert len(schedule.scheduled_tasks) == 3
        assert schedule.total_duration_minutes == 50  # 15 + 25 + 10
    
    def test_remove_scheduled_task(self):
        """Test removing scheduled tasks."""
        schedule = Schedule(datetime(2024, 1, 1))
        task1 = ScheduledTask(Task("Keep", 20), datetime(2024, 1, 1, 9, 0))
        task2 = ScheduledTask(Task("Remove", 30), datetime(2024, 1, 1, 10, 0))
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        schedule.remove_scheduled_task(task2)
        
        assert len(schedule.scheduled_tasks) == 1
        assert task1 in schedule.scheduled_tasks
        assert task2 not in schedule.scheduled_tasks
        assert schedule.total_duration_minutes == 20
    
    def test_remove_nonexistent_scheduled_task(self):
        """Test removing non-existent scheduled task."""
        schedule = Schedule(datetime(2024, 1, 1))
        fake_task = ScheduledTask(Task("Fake", 10), datetime.now())
        
        # Should not raise error
        schedule.remove_scheduled_task(fake_task)
        assert len(schedule.scheduled_tasks) == 0
    
    def test_get_scheduled_tasks_sorted(self):
        """Test that get_scheduled_tasks returns tasks sorted by time."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Add tasks in reverse chronological order
        task_3pm = ScheduledTask(Task("Late", 10), datetime(2024, 1, 1, 15, 0))
        task_9am = ScheduledTask(Task("Early", 10), datetime(2024, 1, 1, 9, 0))
        task_12pm = ScheduledTask(Task("Noon", 10), datetime(2024, 1, 1, 12, 0))
        
        schedule.add_scheduled_task(task_3pm)
        schedule.add_scheduled_task(task_9am)
        schedule.add_scheduled_task(task_12pm)
        
        sorted_tasks = schedule.get_scheduled_tasks()
        
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0] == task_9am
        assert sorted_tasks[1] == task_12pm
        assert sorted_tasks[2] == task_3pm
    
    def test_get_total_duration(self):
        """Test getting total duration."""
        schedule = Schedule(datetime(2024, 1, 1))
        assert schedule.get_total_duration() == 0
        
        schedule.add_scheduled_task(ScheduledTask(Task("Test", 45), datetime.now()))
        assert schedule.get_total_duration() == 45
    
    def test_has_conflicts_no_conflicts(self):
        """Test conflict detection with no conflicts."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Non-overlapping tasks
        task1 = ScheduledTask(Task("First", 30), datetime(2024, 1, 1, 9, 0))   # 9:00-9:30
        task2 = ScheduledTask(Task("Second", 20), datetime(2024, 1, 1, 10, 0)) # 10:00-10:20
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        assert not schedule.has_conflicts()
    
    def test_has_conflicts_with_conflicts(self):
        """Test conflict detection with overlapping tasks."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Overlapping tasks
        task1 = ScheduledTask(Task("First", 60), datetime(2024, 1, 1, 9, 0))   # 9:00-10:00
        task2 = ScheduledTask(Task("Second", 30), datetime(2024, 1, 1, 9, 30)) # 9:30-10:00
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        assert schedule.has_conflicts()
    
    def test_get_detailed_conflicts(self):
        """Test getting detailed conflict information."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        task1 = ScheduledTask(Task("First", 60), datetime(2024, 1, 1, 9, 0))   # 9:00-10:00
        task2 = ScheduledTask(Task("Second", 45), datetime(2024, 1, 1, 9, 30)) # 9:30-10:15
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        conflicts = schedule.get_detailed_conflicts()
        
        assert len(conflicts) == 1
        conflict = conflicts[0]
        assert conflict['task1'] == task1
        assert conflict['task2'] == task2
        assert conflict['overlap_start'] == datetime(2024, 1, 1, 9, 30)
        assert conflict['overlap_end'] == datetime(2024, 1, 1, 10, 0)
        assert conflict['conflict_type'] == 'time_overlap'
    
    def test_get_detailed_conflicts_multiple(self):
        """Test getting multiple conflicts."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Three overlapping tasks
        task1 = ScheduledTask(Task("First", 120), datetime(2024, 1, 1, 9, 0))   # 9:00-11:00
        task2 = ScheduledTask(Task("Second", 60), datetime(2024, 1, 1, 9, 30))  # 9:30-10:30
        task3 = ScheduledTask(Task("Third", 90), datetime(2024, 1, 1, 10, 0))   # 10:00-11:30
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        schedule.add_scheduled_task(task3)
        
        conflicts = schedule.get_detailed_conflicts()
        
        # Should detect 3 conflicts: 1-2, 1-3, 2-3
        assert len(conflicts) == 3
    
    def test_get_free_time_slots_empty_schedule(self):
        """Test getting free time slots from empty schedule."""
        schedule = Schedule(datetime(2024, 1, 1))
        free_slots = schedule.get_free_time_slots()
        assert len(free_slots) == 0
    
    def test_get_free_time_slots_single_task(self):
        """Test getting free time slots with single task."""
        schedule = Schedule(datetime(2024, 1, 1))
        task = ScheduledTask(Task("Only", 30), datetime(2024, 1, 1, 10, 0))
        schedule.add_scheduled_task(task)
        
        free_slots = schedule.get_free_time_slots()
        assert len(free_slots) == 0  # No gaps with single task
    
    def test_get_free_time_slots_with_gaps(self):
        """Test getting free time slots with gaps between tasks."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        task1 = ScheduledTask(Task("Morning", 30), datetime(2024, 1, 1, 9, 0))   # 9:00-9:30
        task2 = ScheduledTask(Task("Afternoon", 45), datetime(2024, 1, 1, 14, 0)) # 2:00-2:45
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        free_slots = schedule.get_free_time_slots()
        
        assert len(free_slots) == 1
        start, end = free_slots[0]
        assert start == datetime(2024, 1, 1, 9, 30)
        assert end == datetime(2024, 1, 1, 14, 0)
    
    def test_get_schedule_summary(self):
        """Test getting schedule summary."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Empty schedule
        summary = schedule.get_schedule_summary()
        assert "0 tasks" in summary
        assert "0.0 hours total" in summary
        assert "no conflicts" in summary
        
        # Schedule with tasks
        task1 = ScheduledTask(Task("First", 30), datetime(2024, 1, 1, 9, 0))
        task2 = ScheduledTask(Task("Second", 60), datetime(2024, 1, 1, 10, 0))
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        summary = schedule.get_schedule_summary()
        assert "2 tasks" in summary
        assert "1.5 hours total" in summary
        assert "no conflicts" in summary
        assert "First: 09:00 AM - First (30 min)" in summary
        assert "Last: 10:00 AM - Second (60 min)" in summary
    
    def test_get_schedule_summary_with_conflicts(self):
        """Test schedule summary with conflicts."""
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Overlapping tasks
        task1 = ScheduledTask(Task("First", 60), datetime(2024, 1, 1, 9, 0))
        task2 = ScheduledTask(Task("Second", 30), datetime(2024, 1, 1, 9, 30))
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        summary = schedule.get_schedule_summary()
        assert "with conflicts" in summary
    
    def test_schedule_string_representation(self):
        """Test schedule string representation."""
        date = datetime(2024, 1, 1)
        schedule = Schedule(date)
        
        # Empty schedule
        assert str(schedule) == "Schedule for January 01, 2024: 0 tasks"
        
        # Schedule with tasks
        schedule.add_scheduled_task(ScheduledTask(Task("Test", 10), datetime.now()))
        assert str(schedule) == "Schedule for January 01, 2024: 1 task"
        
        schedule.add_scheduled_task(ScheduledTask(Task("Test2", 10), datetime.now()))
        assert str(schedule) == "Schedule for January 01, 2024: 2 tasks"


class TestSchedulingConstraints:
    """Test SchedulingConstraints class functionality including edge cases."""
    
    def test_constraints_creation_basic(self):
        """Test basic constraints creation."""
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        
        constraints = SchedulingConstraints(start, end)
        
        assert constraints.start_time == start
        assert constraints.end_time == end
        assert constraints.max_total_duration == 480  # 8 hours default
        assert constraints.excluded_categories == []
        assert constraints.time_preferences == {}
        assert not constraints.allow_overlap
    
    def test_constraints_creation_with_params(self):
        """Test constraints creation with all parameters."""
        start = datetime(2024, 1, 1, 9, 0)
        end = datetime(2024, 1, 1, 17, 0)
        
        constraints = SchedulingConstraints(
            start, end, 300, ["training"], {"feeding": "morning"}, True
        )
        
        assert constraints.start_time == start
        assert constraints.end_time == end
        assert constraints.max_total_duration == 300
        assert constraints.excluded_categories == ["training"]
        assert constraints.time_preferences == {"feeding": "morning"}
        assert constraints.allow_overlap
    
    def test_add_exclusion(self):
        """Test adding category exclusions."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now())
        
        constraints.add_exclusion(TaskCategory.TRAINING)
        constraints.add_exclusion(TaskCategory.GROOMING)
        
        assert "training" in constraints.excluded_categories
        assert "grooming" in constraints.excluded_categories
        assert len(constraints.excluded_categories) == 2
    
    def test_add_exclusion_duplicate(self):
        """Test adding duplicate exclusions."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now())
        
        constraints.add_exclusion(TaskCategory.TRAINING)
        constraints.add_exclusion(TaskCategory.TRAINING)  # Duplicate
        
        assert len(constraints.excluded_categories) == 1
    
    def test_add_exclusion_string(self):
        """Test adding exclusions as strings."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now())
        constraints.add_exclusion("custom_category")
        
        assert "custom_category" in constraints.excluded_categories
    
    def test_set_time_preference(self):
        """Test setting time preferences."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now())
        
        constraints.set_time_preference(TaskCategory.FEEDING, TimeOfDay.MORNING)
        constraints.set_time_preference(TaskCategory.GROOMING, TimeOfDay.AFTERNOON)
        
        assert constraints.time_preferences["feeding"] == "morning"
        assert constraints.time_preferences["grooming"] == "afternoon"
    
    def test_set_time_preference_string(self):
        """Test setting time preferences with strings."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now())
        constraints.set_time_preference("custom_category", "evening")
        
        assert constraints.time_preferences["custom_category"] == "evening"
    
    def test_is_time_allowed_outside_window(self):
        """Test time allowance outside time window."""
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        # Too early
        too_early = datetime(2024, 1, 1, 7, 0)
        assert not constraints.is_time_allowed(too_early, TaskCategory.FEEDING)
        
        # Too late
        too_late = datetime(2024, 1, 1, 19, 0)
        assert not constraints.is_time_allowed(too_late, TaskCategory.FEEDING)
        
        # Just right
        good_time = datetime(2024, 1, 1, 10, 0)
        assert constraints.is_time_allowed(good_time, TaskCategory.FEEDING)
    
    def test_is_time_allowed_excluded_category(self):
        """Test time allowance for excluded categories."""
        constraints = SchedulingConstraints(datetime(2024, 1, 1, 8, 0), datetime(2024, 1, 1, 18, 0))
        constraints.add_exclusion(TaskCategory.TRAINING)
        
        good_time = datetime(2024, 1, 1, 10, 0)
        
        assert not constraints.is_time_allowed(good_time, TaskCategory.TRAINING)
        assert constraints.is_time_allowed(good_time, TaskCategory.FEEDING)
    
    def test_is_time_allowed_time_preference_match(self):
        """Test time allowance with matching time preferences."""
        start = datetime(2024, 1, 1, 6, 0)
        end = datetime(2024, 1, 1, 22, 0)
        constraints = SchedulingConstraints(start, end)
        constraints.set_time_preference(TaskCategory.FEEDING, TimeOfDay.MORNING)
        
        # Morning time (8-10 AM) should be allowed for feeding
        morning_time = datetime(2024, 1, 1, 9, 0)
        assert constraints.is_time_allowed(morning_time, TaskCategory.FEEDING)
        
        # Afternoon time should not be allowed for feeding
        afternoon_time = datetime(2024, 1, 1, 15, 0)
        assert not constraints.is_time_allowed(afternoon_time, TaskCategory.FEEDING)
    
    def test_is_time_allowed_no_preference(self):
        """Test time allowance with no specific preference."""
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        # Should allow any time within window for categories without preferences
        test_time = datetime(2024, 1, 1, 12, 0)
        assert constraints.is_time_allowed(test_time, TaskCategory.EXERCISE)
    
    def test_get_remaining_time(self):
        """Test getting remaining available time."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now(), 480)  # 8 hours
        
        assert constraints.get_remaining_time(0) == 480
        assert constraints.get_remaining_time(120) == 360  # 480 - 120
        assert constraints.get_remaining_time(500) == 0    # Over limit, returns 0
    
    def test_get_remaining_time_negative(self):
        """Test remaining time calculation with over-allocation."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now(), 240)  # 4 hours
        assert constraints.get_remaining_time(300) == 0  # Should not return negative
    
    def test_time_in_preference_all_ranges(self):
        """Test all time preference ranges."""
        constraints = SchedulingConstraints(datetime(2024, 1, 1, 0, 0), datetime(2024, 1, 1, 23, 59))
        
        test_cases = [
            (datetime(2024, 1, 1, 7, 0), "early_morning", True),
            (datetime(2024, 1, 1, 9, 0), "morning", True),
            (datetime(2024, 1, 1, 11, 0), "late_morning", True),
            (datetime(2024, 1, 1, 13, 0), "afternoon", True),
            (datetime(2024, 1, 1, 17, 0), "evening", True),
            (datetime(2024, 1, 1, 20, 0), "night", True),
            (datetime(2024, 1, 1, 5, 0), "early_morning", False),  # Too early
            (datetime(2024, 1, 1, 23, 0), "night", False),  # Too late
        ]
        
        for test_time, preference, expected in test_cases:
            result = constraints._is_time_in_preference(test_time, preference)
            assert result == expected, f"Failed for {test_time.hour}:00 with preference '{preference}'"
    
    def test_time_in_preference_unknown(self):
        """Test unknown time preference."""
        constraints = SchedulingConstraints(datetime.now(), datetime.now())
        test_time = datetime(2024, 1, 1, 12, 0)
        
        # Unknown preference should return True (allow it)
        assert constraints._is_time_in_preference(test_time, "unknown_preference")
    
    def test_constraints_string_representation(self):
        """Test constraints string representation."""
        start = datetime(2024, 1, 1, 8, 30)
        end = datetime(2024, 1, 1, 17, 45)
        constraints = SchedulingConstraints(start, end, 360)
        
        expected = "Constraints: 08:30 AM - 05:45 PM, max 360 min"
        assert str(constraints) == expected
    
    def test_constraints_edge_case_same_start_end(self):
        """Test constraints with same start and end time."""
        time = datetime(2024, 1, 1, 12, 0)
        constraints = SchedulingConstraints(time, time)
        
        # With the current implementation using <=, the exact boundary time is allowed
        assert constraints.is_time_allowed(time, TaskCategory.GENERAL)
        
        # But a time slightly after should not be allowed
        later_time = datetime(2024, 1, 1, 12, 1)
        assert not constraints.is_time_allowed(later_time, TaskCategory.GENERAL)
    
    def test_constraints_end_before_start(self):
        """Test constraints with end time before start time."""
        start = datetime(2024, 1, 1, 18, 0)
        end = datetime(2024, 1, 1, 8, 0)  # Next day 8 AM, but same date
        
        constraints = SchedulingConstraints(start, end)
        
        # Should handle gracefully - no times would be valid
        test_time = datetime(2024, 1, 1, 10, 0)
        assert not constraints.is_time_allowed(test_time, TaskCategory.GENERAL)


class TestSchedulerCore:
    """Test Scheduler class core functionality including edge cases."""
    
    def test_scheduler_creation(self):
        """Test basic scheduler creation."""
        owner = Owner("Test Owner")
        scheduler = Scheduler(owner)
        
        assert scheduler.owner == owner
        assert scheduler.available_tasks == []
        assert scheduler.scheduling_rules == {}
        assert Priority.CRITICAL in scheduler.priority_weights
        assert scheduler.priority_weights[Priority.CRITICAL] == 4
    
    def test_add_task(self):
        """Test adding tasks to scheduler."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task1 = Task("Task 1", 30)
        task2 = Task("Task 2", 45)
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        assert len(scheduler.available_tasks) == 2
        assert task1 in scheduler.available_tasks
        assert task2 in scheduler.available_tasks
    
    def test_add_duplicate_task(self):
        """Test adding same task multiple times."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        task = Task("Duplicate", 20)
        
        scheduler.add_task(task)
        scheduler.add_task(task)  # Should not add duplicate
        
        assert len(scheduler.available_tasks) == 1
    
    def test_remove_task(self):
        """Test removing tasks from scheduler."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task1 = Task("Keep", 30)
        task2 = Task("Remove", 45)
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        scheduler.remove_task(task2)
        
        assert len(scheduler.available_tasks) == 1
        assert task1 in scheduler.available_tasks
        assert task2 not in scheduler.available_tasks
    
    def test_remove_nonexistent_task(self):
        """Test removing task that doesn't exist."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        fake_task = Task("Fake", 10)
        
        # Should not raise error
        scheduler.remove_task(fake_task)
        assert len(scheduler.available_tasks) == 0
    
    def test_sort_by_time_empty_list(self):
        """Test sorting empty list of scheduled tasks."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        result = scheduler.sort_by_time([])
        assert result == []
    
    def test_sort_by_time_single_task(self):
        """Test sorting single scheduled task."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task = ScheduledTask(Task("Single", 10), datetime(2024, 1, 1, 10, 0))
        result = scheduler.sort_by_time([task])
        
        assert len(result) == 1
        assert result[0] == task
    
    def test_sort_by_time_multiple_tasks(self):
        """Test sorting multiple scheduled tasks by time."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task_3pm = ScheduledTask(Task("Late", 10), datetime(2024, 1, 1, 15, 0))
        task_9am = ScheduledTask(Task("Early", 10), datetime(2024, 1, 1, 9, 0))
        task_12pm = ScheduledTask(Task("Noon", 10), datetime(2024, 1, 1, 12, 0))
        
        tasks = [task_3pm, task_9am, task_12pm]
        result = scheduler.sort_by_time(tasks)
        
        assert len(result) == 3
        assert result[0] == task_9am
        assert result[1] == task_12pm
        assert result[2] == task_3pm
    
    def test_sort_by_time_same_time(self):
        """Test sorting tasks with identical times."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        time = datetime(2024, 1, 1, 10, 0)
        task1 = ScheduledTask(Task("First", 10), time)
        task2 = ScheduledTask(Task("Second", 10), time)
        
        result = scheduler.sort_by_time([task2, task1])
        
        # Should maintain stable sort
        assert len(result) == 2
    
    def test_filter_tasks_by_pet(self):
        """Test filtering tasks by pet applicability."""
        dog = Pet("Buddy", "dog", 3)
        cat = Pet("Whiskers", "cat", 5)
        owner = Owner("Test")
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        scheduler = Scheduler(owner)
        
        dog_task = Task("Dog Task", 30)
        dog_task.add_species_requirement("dog")
        
        cat_task = Task("Cat Task", 20)
        cat_task.add_species_requirement("cat")
        
        general_task = Task("General Task", 15)
        
        scheduler.add_task(dog_task)
        scheduler.add_task(cat_task)
        scheduler.add_task(general_task)
        
        dog_applicable = scheduler.filter_tasks_by_pet(dog)
        cat_applicable = scheduler.filter_tasks_by_pet(cat)
        
        assert len(dog_applicable) == 2  # dog_task + general_task
        assert dog_task in dog_applicable
        assert general_task in dog_applicable
        assert cat_task not in dog_applicable
        
        assert len(cat_applicable) == 2  # cat_task + general_task
        assert cat_task in cat_applicable
        assert general_task in cat_applicable
        assert dog_task not in cat_applicable
    
    def test_filter_scheduled_tasks_by_status(self):
        """Test filtering scheduled tasks by status."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        pending_task = ScheduledTask(Task("Pending", 10), datetime.now())
        completed_task = ScheduledTask(Task("Completed", 10), datetime.now())
        completed_task.set_status(TaskStatus.COMPLETED)
        
        schedule.add_scheduled_task(pending_task)
        schedule.add_scheduled_task(completed_task)
        
        pending_filtered = scheduler.filter_scheduled_tasks_by_status(schedule, TaskStatus.PENDING)
        completed_filtered = scheduler.filter_scheduled_tasks_by_status(schedule, TaskStatus.COMPLETED)
        
        assert len(pending_filtered) == 1
        assert pending_task in pending_filtered
        
        assert len(completed_filtered) == 1
        assert completed_task in completed_filtered
    
    def test_filter_tasks_by_category(self):
        """Test filtering tasks by category."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        feeding_task = Task("Feed", 10, category=TaskCategory.FEEDING)
        exercise_task = Task("Walk", 30, category=TaskCategory.EXERCISE)
        grooming_task = Task("Brush", 15, category=TaskCategory.GROOMING)
        
        scheduler.add_task(feeding_task)
        scheduler.add_task(exercise_task)
        scheduler.add_task(grooming_task)
        
        feeding_filtered = scheduler.filter_tasks_by_category(TaskCategory.FEEDING)
        exercise_filtered = scheduler.filter_tasks_by_category(TaskCategory.EXERCISE)
        
        assert len(feeding_filtered) == 1
        assert feeding_task in feeding_filtered
        
        assert len(exercise_filtered) == 1
        assert exercise_task in exercise_filtered
    
    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by minimum priority."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        low_task = Task("Low", 10, Priority.LOW)
        medium_task = Task("Medium", 10, Priority.MEDIUM)
        high_task = Task("High", 10, Priority.HIGH)
        critical_task = Task("Critical", 10, Priority.CRITICAL)
        
        scheduler.add_task(low_task)
        scheduler.add_task(medium_task)
        scheduler.add_task(high_task)
        scheduler.add_task(critical_task)
        
        # Filter for MEDIUM and above
        medium_and_above = scheduler.filter_tasks_by_priority(Priority.MEDIUM)
        
        assert len(medium_and_above) == 3
        assert medium_task in medium_and_above
        assert high_task in medium_and_above
        assert critical_task in medium_and_above
        assert low_task not in medium_and_above
    
    def test_set_scheduling_rule(self):
        """Test setting custom scheduling rules."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        def custom_rule(task):
            return task.duration_minutes < 60
        
        scheduler.set_scheduling_rule("short_tasks_only", custom_rule)
        
        assert "short_tasks_only" in scheduler.scheduling_rules
        assert scheduler.scheduling_rules["short_tasks_only"] == custom_rule
    
    def test_set_priority_weight(self):
        """Test setting custom priority weights."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        scheduler.set_priority_weight(Priority.LOW, 10)
        
        assert scheduler.priority_weights[Priority.LOW] == 10
    
    def test_score_task_basic(self):
        """Test basic task scoring."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        task = Task("Test", 30, Priority.HIGH)
        time = datetime(2024, 1, 1, 10, 0)
        
        score = scheduler.score_task(task, dog, time)
        
        # Should be base priority (3 for HIGH)
        assert score == 3.0
    
    def test_score_task_overdue_bonus(self):
        """Test task scoring with overdue bonus."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task = Task("Overdue", 30, Priority.LOW)
        task.set_recurring(1)
        task.last_completed = datetime.now() - timedelta(days=2)
        
        time = datetime(2024, 1, 1, 10, 0)
        score = scheduler.score_task(task, dog, time)
        
        # Should be 1 (LOW) + 5 (overdue bonus) = 6
        assert score == 6.0
    
    def test_score_task_time_preference_bonus(self):
        """Test task scoring with time preference bonus."""
        dog = Pet("Buddy", "dog", 3)
        dog.add_preference("exercise_time", "morning")
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task = Task("Exercise", 30, Priority.LOW, TaskCategory.EXERCISE)
        morning_time = datetime(2024, 1, 1, 9, 0)  # 9 AM is morning
        
        score = scheduler.score_task(task, dog, morning_time)
        
        # Should be 1 (LOW) + 2 (time preference bonus) = 3
        assert score == 3.0
    
    def test_score_task_energy_matching_bonus(self):
        """Test task scoring with energy level matching bonus."""
        dog = Pet("Buddy", "dog", 3)
        dog.set_energy_level(EnergyLevel.HIGH)
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task = Task("High Energy Task", 30, Priority.LOW)
        task.add_energy_requirement(EnergyLevel.HIGH)
        
        time = datetime(2024, 1, 1, 10, 0)
        score = scheduler.score_task(task, dog, time)
        
        # Should be 1 (LOW) + 1 (energy matching bonus) = 2
        assert score == 2.0
    
    def test_complete_task_and_handle_recurring(self):
        """Test completing recurring tasks and auto-generation."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        recurring_task = Task("Daily Task", 30)
        recurring_task.set_recurring(1)
        
        scheduled = ScheduledTask(recurring_task, datetime.now())
        
        next_task = scheduler.complete_task_and_handle_recurring(scheduled)
        
        assert scheduled.status == TaskStatus.COMPLETED
        assert next_task is not None
        assert next_task.title == "Daily Task"
        assert next_task in scheduler.available_tasks
    
    def test_complete_task_non_recurring(self):
        """Test completing non-recurring tasks."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task = Task("One-time", 30)
        scheduled = ScheduledTask(task, datetime.now())
        
        next_task = scheduler.complete_task_and_handle_recurring(scheduled)
        
        assert scheduled.status == TaskStatus.COMPLETED
        assert next_task is None
    
    def test_validate_schedule_valid(self):
        """Test validating a valid schedule."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        task = Task("Dog Task", 30)
        task.add_species_requirement("dog")
        scheduled = ScheduledTask(task, datetime(2024, 1, 1, 10, 0))
        
        schedule.add_scheduled_task(scheduled)
        
        assert scheduler.validate_schedule(schedule)
    
    def test_validate_schedule_with_conflicts(self):
        """Test validating schedule with conflicts."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Overlapping tasks
        task1 = ScheduledTask(Task("First", 60), datetime(2024, 1, 1, 9, 0))
        task2 = ScheduledTask(Task("Second", 30), datetime(2024, 1, 1, 9, 30))
        
        schedule.add_scheduled_task(task1)
        schedule.add_scheduled_task(task2)
        
        assert not scheduler.validate_schedule(schedule)
    
    def test_validate_schedule_inapplicable_tasks(self):
        """Test validating schedule with inapplicable tasks."""
        cat = Pet("Whiskers", "cat", 5)
        owner = Owner("Test")
        owner.add_pet(cat)
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Dog-only task for cat owner
        dog_task = Task("Dog Walk", 30)
        dog_task.add_species_requirement("dog")
        scheduled = ScheduledTask(dog_task, datetime(2024, 1, 1, 10, 0))
        
        schedule.add_scheduled_task(scheduled)
        
        assert not scheduler.validate_schedule(schedule)


class TestSchedulerAdvanced:
    """Test advanced Scheduler functionality and edge cases."""
    
    def test_find_optimal_time_slot_no_constraints_violation(self):
        """Test finding optimal time slot without constraint violations."""
        owner = Owner("Test")
        # Add a pet so the scoring algorithm can work
        pet = Pet("TestPet", "dog", 3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task = Task("Test Task", 60)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        time_slot = scheduler.find_optimal_time_slot(task, constraints)
        
        assert time_slot is not None
        assert time_slot >= start
        assert time_slot + timedelta(minutes=60) <= end
    
    def test_find_optimal_time_slot_no_space(self):
        """Test finding optimal time slot when no space available."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        task = Task("Long Task", 120)  # 2 hours
        
        # Very tight constraint - only 1 hour available
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 9, 0)
        constraints = SchedulingConstraints(start, end)
        
        time_slot = scheduler.find_optimal_time_slot(task, constraints)
        
        assert time_slot is None
    
    def test_find_optimal_time_slot_with_conflicts(self):
        """Test finding optimal time slot with existing schedule conflicts."""
        owner = Owner("Test")
        # Add a pet so the scoring algorithm can work
        pet = Pet("TestPet", "dog", 3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task = Task("New Task", 60)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        # Create existing schedule with conflict
        current_schedule = Schedule(datetime(2024, 1, 1))
        existing_task = ScheduledTask(Task("Existing", 120), datetime(2024, 1, 1, 8, 0))  # 8-10 AM
        current_schedule.add_scheduled_task(existing_task)
        
        time_slot = scheduler.find_optimal_time_slot(task, constraints, current_schedule)
        
        assert time_slot is not None
        # Should find slot after 10 AM
        assert time_slot >= datetime(2024, 1, 1, 10, 0)
    
    def test_detect_pet_conflicts_no_conflicts(self):
        """Test pet conflict detection with no conflicts."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Non-overlapping tasks for same pet
        task1 = Task("First", 30)
        task1.add_species_requirement("dog")
        scheduled1 = ScheduledTask(task1, datetime(2024, 1, 1, 9, 0))
        
        task2 = Task("Second", 30)
        task2.add_species_requirement("dog")
        scheduled2 = ScheduledTask(task2, datetime(2024, 1, 1, 10, 0))
        
        schedule.add_scheduled_task(scheduled1)
        schedule.add_scheduled_task(scheduled2)
        
        conflicts = scheduler.detect_pet_conflicts(schedule)
        
        assert len(conflicts) == 0
    
    def test_detect_pet_conflicts_with_conflicts(self):
        """Test pet conflict detection with overlapping tasks."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Overlapping tasks for same pet
        task1 = Task("First", 60)
        task1.add_species_requirement("dog")
        scheduled1 = ScheduledTask(task1, datetime(2024, 1, 1, 9, 0))  # 9-10 AM
        
        task2 = Task("Second", 30)
        task2.add_species_requirement("dog")
        scheduled2 = ScheduledTask(task2, datetime(2024, 1, 1, 9, 30))  # 9:30-10 AM
        
        schedule.add_scheduled_task(scheduled1)
        schedule.add_scheduled_task(scheduled2)
        
        conflicts = scheduler.detect_pet_conflicts(schedule)
        
        assert "Buddy" in conflicts
        assert len(conflicts["Buddy"]) == 1
        
        conflict = conflicts["Buddy"][0]
        assert conflict['task1'] == 'First'
        assert conflict['task2'] == 'Second'
        assert conflict['overlap_duration_minutes'] == 30
    
    def test_detect_resource_conflicts(self):
        """Test resource (owner) conflict detection."""
        dog = Pet("Buddy", "dog", 3)
        cat = Pet("Whiskers", "cat", 5)
        owner = Owner("Test")
        owner.add_pet(dog)
        owner.add_pet(cat)
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        # Overlapping tasks for different pets (owner conflict)
        dog_task = Task("Dog Walk", 60)
        dog_task.add_species_requirement("dog")
        dog_scheduled = ScheduledTask(dog_task, datetime(2024, 1, 1, 9, 0))
        
        cat_task = Task("Cat Grooming", 30)
        cat_task.add_species_requirement("cat")
        cat_scheduled = ScheduledTask(cat_task, datetime(2024, 1, 1, 9, 30))
        
        schedule.add_scheduled_task(dog_scheduled)
        schedule.add_scheduled_task(cat_scheduled)
        
        conflicts = scheduler.detect_resource_conflicts(schedule)
        
        assert len(conflicts) == 1
        conflict = conflicts[0]
        assert conflict['conflict_type'] == 'owner_availability'
        assert 'Buddy' in conflict['pets1']
        assert 'Whiskers' in conflict['pets2']
    
    def test_explain_scheduling_decisions(self):
        """Test getting scheduling decision explanations."""
        owner = Owner("Test")
        scheduler = Scheduler(owner)
        
        schedule = Schedule(datetime(2024, 1, 1))
        
        task = Task("Test Task", 30)
        reason = "High priority and optimal time"
        scheduled = ScheduledTask(task, datetime(2024, 1, 1, 10, 0), reason)
        
        schedule.add_scheduled_task(scheduled)
        
        explanations = scheduler.explain_scheduling_decisions(schedule)
        
        assert "Test Task" in explanations
        assert explanations["Test Task"] == reason
    
    def test_generate_daily_schedule_empty_owner(self):
        """Test generating schedule for owner with no pets."""
        owner = Owner("Empty")
        scheduler = Scheduler(owner)
        
        task = Task("General Task", 30)
        scheduler.add_task(task)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        schedule = scheduler.generate_daily_schedule(datetime(2024, 1, 1), constraints)
        
        # Should create empty schedule since no pets to assign tasks to
        assert len(schedule.scheduled_tasks) == 0
    
    def test_generate_daily_schedule_no_tasks(self):
        """Test generating schedule with no available tasks."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        schedule = scheduler.generate_daily_schedule(datetime(2024, 1, 1), constraints)
        
        assert len(schedule.scheduled_tasks) == 0
    
    def test_generate_daily_schedule_basic(self):
        """Test basic daily schedule generation."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        # Add applicable tasks
        task1 = Task("Dog Walk", 30, Priority.HIGH)
        task1.add_species_requirement("dog")
        
        task2 = Task("Feed Dog", 10, Priority.CRITICAL)
        task2.add_species_requirement("dog")
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        
        schedule = scheduler.generate_daily_schedule(datetime(2024, 1, 1), constraints)
        
        assert len(schedule.scheduled_tasks) == 2
        # Should be sorted by time
        sorted_tasks = schedule.get_scheduled_tasks()
        assert len(sorted_tasks) == 2
    
    def test_generate_daily_schedule_time_limit(self):
        """Test schedule generation with time limit constraints."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        # Add many tasks that would exceed time limit
        for i in range(10):
            task = Task(f"Task {i}", 60, Priority.MEDIUM)  # Each 1 hour
            task.add_species_requirement("dog")
            scheduler.add_task(task)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end, max_total_duration=120)  # 2 hours max
        
        schedule = scheduler.generate_daily_schedule(datetime(2024, 1, 1), constraints)
        
        # Should stop at time limit
        assert schedule.get_total_duration() <= 120
    
    def test_generate_daily_schedule_with_exclusions(self):
        """Test schedule generation with excluded categories."""
        dog = Pet("Buddy", "dog", 3)
        owner = Owner("Test")
        owner.add_pet(dog)
        scheduler = Scheduler(owner)
        
        feeding_task = Task("Feed", 10, category=TaskCategory.FEEDING)
        feeding_task.add_species_requirement("dog")
        
        training_task = Task("Train", 30, category=TaskCategory.TRAINING)
        training_task.add_species_requirement("dog")
        
        scheduler.add_task(feeding_task)
        scheduler.add_task(training_task)
        
        start = datetime(2024, 1, 1, 8, 0)
        end = datetime(2024, 1, 1, 18, 0)
        constraints = SchedulingConstraints(start, end)
        constraints.add_exclusion(TaskCategory.TRAINING)
        
        schedule = scheduler.generate_daily_schedule(datetime(2024, 1, 1), constraints)
        
        # Should only include feeding task
        assert len(schedule.scheduled_tasks) == 1
        assert schedule.scheduled_tasks[0].task.category == TaskCategory.FEEDING
