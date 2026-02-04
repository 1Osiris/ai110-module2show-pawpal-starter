import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path to import pawpal_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import (
    Pet, Task, Owner, Scheduler, ScheduledTask,
    Priority, TaskCategory, TaskStatus, EnergyLevel
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
