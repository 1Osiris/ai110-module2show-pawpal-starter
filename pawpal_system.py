"""
PawPal+ System - Pet Care Task Scheduling System
Based on UML design in system_design_fixed.mmd
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Status of a scheduled task."""
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    IN_PROGRESS = "in_progress"


class TimeOfDay(Enum):
    """Preferred times of day for activities."""
    EARLY_MORNING = "early_morning"  # 6-8 AM
    MORNING = "morning"              # 8-10 AM
    LATE_MORNING = "late_morning"    # 10 AM-12 PM
    AFTERNOON = "afternoon"          # 12-4 PM
    EVENING = "evening"              # 4-7 PM
    NIGHT = "night"                  # 7-10 PM


class EnergyLevel(Enum):
    """Pet energy levels affecting task scheduling."""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ActivityPreference(Enum):
    """Common pet activity preferences."""
    INDOOR_ONLY = "indoor_only"
    OUTDOOR_PREFERRED = "outdoor_preferred"
    MIXED = "mixed"
    SOCIAL = "social"           # Prefers activities with other pets/people
    SOLITARY = "solitary"       # Prefers solo activities
    GENTLE = "gentle"           # Prefers calm, low-intensity activities
    ACTIVE = "active"           # Prefers high-energy activities


class MedicalCondition(Enum):
    """Common pet medical conditions affecting scheduling."""
    ARTHRITIS = "arthritis"
    HIP_DYSPLASIA = "hip_dysplasia"
    HEART_CONDITION = "heart_condition"
    DIABETES = "diabetes"
    ANXIETY = "anxiety"
    SENIOR_MOBILITY = "senior_mobility"
    RECOVERING_FROM_SURGERY = "recovering_from_surgery"
    OVERWEIGHT = "overweight"
    UNDERWEIGHT = "underweight"
    MEDICATION_SCHEDULE = "medication_schedule"
    ALLERGIES = "allergies"


class TaskCategory(Enum):
    """Categories of pet care tasks."""
    FEEDING = "feeding"
    EXERCISE = "exercise"
    GROOMING = "grooming"
    MEDICAL = "medical"
    TRAINING = "training"
    ENRICHMENT = "enrichment"
    SOCIAL = "social"
    MAINTENANCE = "maintenance"  # Litter box, cage cleaning, etc.
    GENERAL = "general"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Pet:
    """Represents a pet with preferences and medical conditions."""
    
    name: str
    species: str
    age: int
    breed: str = ""
    preferences: dict = field(default_factory=dict)
    medical_conditions: dict = field(default_factory=dict)
    
    def add_preference(self, key: str, value: str) -> None:
        """Add a preference for the pet (e.g., 'walk_time': 'morning')."""
        pass
    
    def get_preferences(self) -> dict:
        """Return all preferences for this pet."""
        pass
    
    def add_medical_condition(self, condition: str, notes: str) -> None:
        """Add a medical condition with notes (e.g., 'arthritis': 'avoid long walks')."""
        pass
    
    def get_medical_conditions(self) -> dict:
        """Return all medical conditions for this pet."""
        pass
    
    def __str__(self) -> str:
        return f"{self.name} ({self.species}, {self.breed}, {self.age} years old)"


@dataclass
class Owner:
    """Represents a pet owner with time constraints and preferences."""
    
    name: str
    available_time_minutes: int = 120
    time_windows: dict = field(default_factory=dict)
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        pass
    
    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's list of pets."""
        pass
    
    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        pass
    
    def set_time_window(self, start_time: datetime, end_time: datetime) -> None:
        """Set the time window when the owner is available."""
        pass
    
    def get_available_time(self) -> int:
        """Return the total available time in minutes."""
        pass
    
    def add_preference(self, key: str, value: str) -> None:
        """Add a scheduling preference."""
        pass
    
    def get_preferences(self) -> dict:
        """Return all owner preferences."""
        pass
    
    def __str__(self) -> str:
        pet_count = len(self.pets)
        return f"{self.name} ({pet_count} pet{'s' if pet_count != 1 else ''})"


# ============================================================================
# TASK CLASSES
# ============================================================================

@dataclass
class Task:
    """Represents an individual pet care task."""
    
    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    category: str = "general"
    is_recurring: bool = False
    frequency_days: int = 0
    requirements: dict = field(default_factory=dict)
    last_completed: Optional[datetime] = None
    
    def set_recurring(self, frequency_days: int) -> None:
        """Set the task to recur every N days."""
        pass
    
    def add_requirement(self, pet_attribute: str, required_value: str) -> None:
        """Add a requirement for this task (e.g., 'species': 'dog')."""
        pass
    
    def is_applicable_for_pet(self, pet: Pet) -> bool:
        """Check if this task is applicable for the given pet."""
        pass
    
    def get_priority_score(self) -> int:
        """Return numeric priority score for sorting."""
        pass
    
    def is_overdue(self) -> bool:
        """Check if this recurring task is overdue based on last completion."""
        pass
    
    def mark_completed(self) -> None:
        """Mark the task as completed and update last_completed timestamp."""
        pass
    
    def __str__(self) -> str:
        return f"{self.title} ({self.duration_minutes} min, {self.priority.name})"


@dataclass
class ScheduledTask:
    """A task with scheduling information attached."""
    
    task: Task
    scheduled_time: datetime
    reason: str = ""
    duration_minutes: int = field(init=False)
    status: TaskStatus = TaskStatus.PENDING
    
    def __post_init__(self):
        """Initialize duration from the referenced task."""
        self.duration_minutes = self.task.duration_minutes
    
    def get_task(self) -> Task:
        """Return the underlying task."""
        pass
    
    def get_scheduled_time(self) -> datetime:
        """Return the scheduled start time."""
        pass
    
    def get_end_time(self) -> datetime:
        """Return the scheduled end time."""
        pass
    
    def set_status(self, status: TaskStatus) -> None:
        """Update the task status."""
        pass
    
    def get_status(self) -> TaskStatus:
        """Return the current status."""
        pass
    
    def get_reason(self) -> str:
        """Return the explanation for why this task was scheduled at this time."""
        pass
    
    def __str__(self) -> str:
        time_str = self.scheduled_time.strftime("%I:%M %p")
        return f"{time_str} - {self.task.title} ({self.duration_minutes} min)"


# ============================================================================
# SCHEDULE CLASSES
# ============================================================================

@dataclass
class Schedule:
    """Container for a day's worth of scheduled tasks."""
    
    date: datetime
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    total_duration_minutes: int = 0
    metadata: dict = field(default_factory=dict)
    
    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Add a scheduled task to this schedule."""
        pass
    
    def remove_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Remove a scheduled task from this schedule."""
        pass
    
    def get_scheduled_tasks(self) -> list[ScheduledTask]:
        """Return all scheduled tasks, sorted by time."""
        pass
    
    def get_total_duration(self) -> int:
        """Return total duration of all tasks in minutes."""
        pass
    
    def has_conflicts(self) -> bool:
        """Check if any scheduled tasks overlap."""
        pass
    
    def get_free_time_slots(self) -> list[tuple[datetime, datetime]]:
        """Return list of free time slots as (start, end) tuples."""
        pass
    
    def get_schedule_summary(self) -> str:
        """Return a human-readable summary of the schedule."""
        pass
    
    def __str__(self) -> str:
        task_count = len(self.scheduled_tasks)
        date_str = self.date.strftime("%B %d, %Y")
        return f"Schedule for {date_str}: {task_count} task{'s' if task_count != 1 else ''}"


# ============================================================================
# CONSTRAINTS CLASS
# ============================================================================

@dataclass
class SchedulingConstraints:
    """Encapsulates all rules and limitations for schedule generation."""
    
    start_time: datetime
    end_time: datetime
    max_total_duration: int = 480  # Default 8 hours
    excluded_categories: list[str] = field(default_factory=list)
    time_preferences: dict = field(default_factory=dict)
    allow_overlap: bool = False
    
    def add_exclusion(self, category: str) -> None:
        """Exclude a category of tasks from scheduling."""
        pass
    
    def set_time_preference(self, category: str, preferred_time: str) -> None:
        """Set a time preference for a category (e.g., 'feeding': 'morning')."""
        pass
    
    def is_time_allowed(self, time_slot: datetime, category: str) -> bool:
        """Check if a task category can be scheduled at the given time."""
        pass
    
    def get_remaining_time(self, current_duration: int) -> int:
        """Return remaining available time given current scheduled duration."""
        pass
    
    def __str__(self) -> str:
        start_str = self.start_time.strftime("%I:%M %p")
        end_str = self.end_time.strftime("%I:%M %p")
        return f"Constraints: {start_str} - {end_str}, max {self.max_total_duration} min"


# ============================================================================
# SCHEDULER CLASS (The Brain)
# ============================================================================

class Scheduler:
    """
    Core scheduling engine that generates optimized daily schedules.
    
    This class takes an owner, their tasks, and constraints to produce
    an optimal schedule that respects priorities, time windows, and
    pet-specific requirements.
    """
    
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner
        self.available_tasks: list[Task] = []
        self.scheduling_rules: dict = {}
        self.priority_weights: dict = {
            Priority.CRITICAL: 4,
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1
        }
    
    def add_task(self, task: Task) -> None:
        """Add a task to the available tasks pool."""
        pass
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the available tasks pool."""
        pass
    
    def set_scheduling_rule(self, rule_name: str, rule_func: callable) -> None:
        """Add a custom scheduling rule."""
        pass
    
    def set_priority_weight(self, priority: Priority, weight: int) -> None:
        """Set the weight for a priority level."""
        pass
    
    def generate_daily_schedule(
        self, 
        date: datetime, 
        constraints: SchedulingConstraints
    ) -> Schedule:
        """
        Generate an optimized daily schedule.
        
        Args:
            date: The date to generate the schedule for
            constraints: SchedulingConstraints object with rules
            
        Returns:
            Schedule object with optimized task assignments
        """
        pass
    
    def score_task(self, task: Task, pet: Pet, time_slot: datetime) -> float:
        """
        Calculate a score for scheduling a task at a given time.
        
        Higher scores indicate better scheduling choices.
        """
        pass
    
    def find_optimal_time_slot(
        self, 
        task: Task, 
        constraints: SchedulingConstraints
    ) -> Optional[datetime]:
        """Find the best time slot for a task given constraints."""
        pass
    
    def validate_schedule(self, schedule: Schedule) -> bool:
        """Validate that a schedule meets all constraints."""
        pass
    
    def explain_scheduling_decisions(self, schedule: Schedule) -> dict:
        """
        Return explanations for why each task was scheduled when it was.
        
        Returns:
            Dict mapping task titles to explanation strings
        """
        pass
    
    # ---- Private Methods ----
    
    def _filter_applicable_tasks(self, pet: Pet) -> list[Task]:
        """Filter tasks that are applicable for the given pet."""
        pass
    
    def _sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority score (highest first)."""
        pass
    
    def _check_time_constraints(
        self, 
        task: Task, 
        time_slot: datetime, 
        constraints: SchedulingConstraints
    ) -> bool:
        """Check if a task can be scheduled at the given time slot."""
        pass


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    # Example usage - this will be expanded during implementation
    
    # Create owner and pet
    owner = Owner(name="Jordan", available_time_minutes=180)
    dog = Pet(name="Mochi", species="dog", age=3, breed="Golden Retriever")
    owner.pets.append(dog)
    
    # Create tasks
    walk = Task(
        title="Morning Walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        category="exercise"
    )
    
    feeding = Task(
        title="Feed Mochi",
        duration_minutes=10,
        priority=Priority.CRITICAL,
        category="feeding"
    )
    
    # Create scheduler and add tasks
    scheduler = Scheduler(owner)
    scheduler.available_tasks.append(walk)
    scheduler.available_tasks.append(feeding)
    
    # Create constraints
    now = datetime.now()
    constraints = SchedulingConstraints(
        start_time=now.replace(hour=7, minute=0),
        end_time=now.replace(hour=19, minute=0),
        max_total_duration=120
    )
    
    # Print skeleton status
    print("PawPal+ System Skeleton Loaded Successfully!")
    print(f"Owner: {owner}")
    print(f"Pet: {dog}")
    print(f"Tasks: {walk}, {feeding}")
    print(f"Constraints: {constraints}")
    print("\nNext step: Implement the method bodies!")
