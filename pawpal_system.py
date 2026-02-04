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
        self.preferences[key] = value
    
    def set_time_preference(self, activity: str, time: TimeOfDay) -> None:
        """Set a time preference using enum (e.g., 'walk', TimeOfDay.MORNING)."""
        self.preferences[f"{activity}_time"] = time.value
    
    def set_energy_level(self, energy: EnergyLevel) -> None:
        """Set the pet's energy level."""
        self.preferences["energy_level"] = energy.value
    
    def set_activity_preference(self, preference: ActivityPreference) -> None:
        """Set activity preference (indoor/outdoor/mixed, etc.)."""
        self.preferences["activity_style"] = preference.value
    
    def get_preferences(self) -> dict:
        """Return all preferences for this pet."""
        return self.preferences.copy()
    
    def add_medical_condition(self, condition: MedicalCondition, notes: str = "") -> None:
        """Add a medical condition with optional notes."""
        self.medical_conditions[condition.value] = notes
    
    def has_medical_condition(self, condition: MedicalCondition) -> bool:
        """Check if pet has a specific medical condition."""
        return condition.value in self.medical_conditions
    
    def get_medical_conditions(self) -> dict:
        """Return all medical conditions for this pet."""
        return self.medical_conditions.copy()
    
    def __str__(self) -> str:
        """Return string representation of the pet."""
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
        if pet not in self.pets:
            self.pets.append(pet)
    
    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's list of pets."""
        if pet in self.pets:
            self.pets.remove(pet)
    
    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets.copy()
    
    def set_time_window(self, start_time: datetime, end_time: datetime) -> None:
        """Set the time window when the owner is available."""
        self.time_windows["default"] = {
            "start": start_time,
            "end": end_time
        }
        # Calculate available time in minutes
        time_diff = end_time - start_time
        self.available_time_minutes = int(time_diff.total_seconds() / 60)
    
    def get_available_time(self) -> int:
        """Return the total available time in minutes."""
        return self.available_time_minutes
    
    def add_preference(self, key: str, value: str) -> None:
        """Add a scheduling preference."""
        self.preferences[key] = value
    
    def get_preferences(self) -> dict:
        """Return all owner preferences."""
        return self.preferences.copy()
    
    def __str__(self) -> str:
        """Return string representation of the owner."""
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
    category: TaskCategory = TaskCategory.GENERAL
    is_recurring: bool = False
    frequency_days: int = 0
    requirements: dict = field(default_factory=dict)
    last_completed: Optional[datetime] = None
    
    def set_recurring(self, frequency_days: int) -> None:
        """Set the task to recur every N days."""
        self.is_recurring = True
        self.frequency_days = frequency_days
    
    def add_species_requirement(self, species: str) -> None:
        """Require a specific species for this task."""
        self.requirements["species"] = species.lower()
    
    def add_medical_restriction(self, condition: MedicalCondition) -> None:
        """Add a medical condition that prevents this task."""
        if "medical_restrictions" not in self.requirements:
            self.requirements["medical_restrictions"] = []
        self.requirements["medical_restrictions"].append(condition.value)
    
    def add_energy_requirement(self, min_energy: EnergyLevel) -> None:
        """Set minimum energy level required for this task."""
        self.requirements["min_energy_level"] = min_energy.value
    
    def is_applicable_for_pet(self, pet: Pet) -> bool:
        """Check if this task is applicable for the given pet."""
        # Check species requirement
        if "species" in self.requirements:
            if pet.species.lower() != self.requirements["species"]:
                return False
        
        # Check medical restrictions
        if "medical_restrictions" in self.requirements:
            for restriction in self.requirements["medical_restrictions"]:
                if restriction in pet.medical_conditions:
                    return False
        
        # Check energy requirements
        if "min_energy_level" in self.requirements:
            pet_energy = pet.preferences.get("energy_level", EnergyLevel.MODERATE.value)
            required_energy = self.requirements["min_energy_level"]
            
            energy_levels = [e.value for e in EnergyLevel]
            if energy_levels.index(pet_energy) < energy_levels.index(required_energy):
                return False
        
        return True
    
    def get_priority_score(self) -> int:
        """Return numeric priority score for sorting."""
        base_score = self.priority.value
        
        # Boost score if overdue
        if self.is_overdue():
            base_score += 2
        
        return base_score
    
    def is_overdue(self) -> bool:
        """Check if this recurring task is overdue based on last completion."""
        if not self.is_recurring or self.last_completed is None:
            return False
        
        days_since_completion = (datetime.now() - self.last_completed).days
        return days_since_completion >= self.frequency_days
    
    def mark_completed(self) -> None:
        """Mark the task as completed and update last_completed timestamp."""
        self.last_completed = datetime.now()
        
        # Auto-create next instance for recurring tasks
        if self.is_recurring:
            self._create_next_recurring_instance()
    
    def _create_next_recurring_instance(self) -> 'Task':
        """Create a new instance of this recurring task for the next occurrence."""
        next_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category
        )
        
        # Copy all requirements
        next_task.requirements = self.requirements.copy()
        next_task.set_recurring(self.frequency_days)
        
        # Set next due date
        if self.last_completed:
            next_due = self.last_completed + timedelta(days=self.frequency_days)
            next_task.last_completed = None  # Reset completion status
        
        return next_task
    
    def __str__(self) -> str:
        """Return string representation of the task."""
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
        return self.task
    
    def get_scheduled_time(self) -> datetime:
        """Return the scheduled start time."""
        return self.scheduled_time
    
    def get_end_time(self) -> datetime:
        """Return the scheduled end time."""
        return self.scheduled_time + timedelta(minutes=self.duration_minutes)
    
    def set_status(self, status: TaskStatus) -> None:
        """Update the task status."""
        self.status = status
        
        # Mark underlying task as completed if status is COMPLETED
        if status == TaskStatus.COMPLETED:
            completed_task = self.task.mark_completed()
            # If this was a recurring task, the mark_completed method created a new instance
            # The calling code should handle adding the new instance to the scheduler
    
    def get_next_recurring_task(self) -> Optional['Task']:
        """Get the next instance of a recurring task if this task was completed."""
        if self.status == TaskStatus.COMPLETED and self.task.is_recurring:
            return self.task._create_next_recurring_instance()
        return None
    
    def get_status(self) -> TaskStatus:
        """Return the current status."""
        return self.status
    
    def get_reason(self) -> str:
        """Return the explanation for why this task was scheduled at this time."""
        return self.reason
    
    def __str__(self) -> str:
        """Return string representation of the scheduled task."""
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
        self.scheduled_tasks.append(scheduled_task)
        self._recalculate_duration()
    
    def remove_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Remove a scheduled task from this schedule."""
        if scheduled_task in self.scheduled_tasks:
            self.scheduled_tasks.remove(scheduled_task)
            self._recalculate_duration()
    
    def get_scheduled_tasks(self) -> list[ScheduledTask]:
        """Return all scheduled tasks, sorted by time."""
        return sorted(self.scheduled_tasks, key=lambda t: t.scheduled_time)
    
    def get_total_duration(self) -> int:
        """Return total duration of all tasks in minutes."""
        return self.total_duration_minutes
    
    def has_conflicts(self) -> bool:
        """Check if any scheduled tasks overlap."""
        return len(self.get_detailed_conflicts()) > 0
    
    def get_detailed_conflicts(self) -> list[dict]:
        """Return detailed information about all scheduling conflicts."""
        conflicts = []
        sorted_tasks = self.get_scheduled_tasks()
        
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task1 = sorted_tasks[i]
                task2 = sorted_tasks[j]
                
                # Check for time overlap
                if self._tasks_overlap(task1, task2):
                    conflicts.append({
                        'task1': task1,
                        'task2': task2,
                        'overlap_start': max(task1.scheduled_time, task2.scheduled_time),
                        'overlap_end': min(task1.get_end_time(), task2.get_end_time()),
                        'conflict_type': 'time_overlap'
                    })
        
        return conflicts
    
    def _tasks_overlap(self, task1: ScheduledTask, task2: ScheduledTask) -> bool:
        """Check if two scheduled tasks have overlapping times."""
        return not (task1.get_end_time() <= task2.scheduled_time or 
                   task2.get_end_time() <= task1.scheduled_time)
    
    def get_free_time_slots(self) -> list[tuple[datetime, datetime]]:
        """Return list of free time slots as (start, end) tuples."""
        free_slots = []
        sorted_tasks = self.get_scheduled_tasks()
        
        if not sorted_tasks:
            return free_slots
        
        # Add gap between tasks
        for i in range(len(sorted_tasks) - 1):
            current_end = sorted_tasks[i].get_end_time()
            next_start = sorted_tasks[i + 1].get_scheduled_time()
            
            if current_end < next_start:
                free_slots.append((current_end, next_start))
        
        return free_slots
    
    def get_schedule_summary(self) -> str:
        """Return a human-readable summary of the schedule."""
        task_count = len(self.scheduled_tasks)
        total_hours = self.total_duration_minutes / 60
        conflicts = "with conflicts" if self.has_conflicts() else "no conflicts"
        
        summary = f"{task_count} task{'s' if task_count != 1 else ''}, "
        summary += f"{total_hours:.1f} hours total, {conflicts}"
        
        if self.scheduled_tasks:
            sorted_tasks = self.get_scheduled_tasks()
            summary += f"\nFirst: {sorted_tasks[0]}"
            if len(sorted_tasks) > 1:
                summary += f"\nLast: {sorted_tasks[-1]}"
        
        return summary
    
    def _recalculate_duration(self) -> None:
        """Recalculate total duration of all scheduled tasks."""
        self.total_duration_minutes = sum(task.duration_minutes for task in self.scheduled_tasks)
    
    def __str__(self) -> str:
        """Return string representation of the schedule."""
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
    
    def add_exclusion(self, category: TaskCategory) -> None:
        """Exclude a category of tasks from scheduling."""
        category_str = category.value if isinstance(category, TaskCategory) else str(category)
        if category_str not in self.excluded_categories:
            self.excluded_categories.append(category_str)
    
    def set_time_preference(self, category: TaskCategory, preferred_time: TimeOfDay) -> None:
        """Set a time preference for a category (e.g., 'feeding': 'morning')."""
        category_str = category.value if isinstance(category, TaskCategory) else str(category)
        time_str = preferred_time.value if isinstance(preferred_time, TimeOfDay) else str(preferred_time)
        self.time_preferences[category_str] = time_str
    
    def is_time_allowed(self, time_slot: datetime, category: TaskCategory) -> bool:
        """Check if a task category can be scheduled at the given time."""
        # Check if time is within allowed window
        if time_slot < self.start_time or time_slot > self.end_time:
            return False
        
        # Check if category is excluded
        category_str = category.value if isinstance(category, TaskCategory) else str(category)
        if category_str in self.excluded_categories:
            return False
        
        # Check time preferences
        if category_str in self.time_preferences:
            preferred_time = self.time_preferences[category_str]
            return self._is_time_in_preference(time_slot, preferred_time)
        
        return True
    
    def get_remaining_time(self, current_duration: int) -> int:
        """Return remaining available time given current scheduled duration."""
        return max(0, self.max_total_duration - current_duration)
    
    def _is_time_in_preference(self, time_slot: datetime, preference: str) -> bool:
        """Check if time slot matches the time preference."""
        hour = time_slot.hour
        
        time_ranges = {
            "early_morning": (6, 8),
            "morning": (8, 10),
            "late_morning": (10, 12),
            "afternoon": (12, 16),
            "evening": (16, 19),
            "night": (19, 22)
        }
        
        if preference in time_ranges:
            start, end = time_ranges[preference]
            return start <= hour < end
        
        return True  # If preference not recognized, allow it
    
    def __str__(self) -> str:
        """Return string representation of the constraints."""
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
        if task not in self.available_tasks:
            self.available_tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the available tasks pool."""
        if task in self.available_tasks:
            self.available_tasks.remove(task)
    
    def sort_by_time(self, scheduled_tasks: list[ScheduledTask]) -> list[ScheduledTask]:
        """Sort scheduled tasks by their scheduled time using merge sort algorithm."""
        if len(scheduled_tasks) <= 1:
            return scheduled_tasks
        
        # Divide the list into two halves
        mid = len(scheduled_tasks) // 2
        left = scheduled_tasks[:mid]
        right = scheduled_tasks[mid:]
        
        # Recursively sort both halves
        left_sorted = self.sort_by_time(left)
        right_sorted = self.sort_by_time(right)
        
        # Merge the sorted halves
        return self._merge_by_time(left_sorted, right_sorted)
    
    def _merge_by_time(self, left: list[ScheduledTask], right: list[ScheduledTask]) -> list[ScheduledTask]:
        """Merge two sorted lists of scheduled tasks by time."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].scheduled_time <= right[j].scheduled_time:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    def filter_tasks_by_pet(self, pet: Pet, include_status: list[TaskStatus] = None) -> list[Task]:
        """Filter tasks applicable to a specific pet with optional status filtering."""
        if include_status is None:
            include_status = [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]
        
        filtered_tasks = []
        
        for task in self.available_tasks:
            if task.is_applicable_for_pet(pet):
                # For basic Task objects, we consider them as PENDING
                # In a real implementation, you might track status differently
                filtered_tasks.append(task)
        
        return filtered_tasks
    
    def filter_scheduled_tasks_by_status(self, schedule, status: TaskStatus) -> list[ScheduledTask]:
        """Filter scheduled tasks by their completion status."""
        return [st for st in schedule.scheduled_tasks if st.status == status]
    
    def filter_tasks_by_category(self, category: TaskCategory) -> list[Task]:
        """Filter tasks by category using linear search."""
        return [task for task in self.available_tasks if task.category == category]
    
    def filter_tasks_by_priority(self, min_priority: Priority) -> list[Task]:
        """Filter tasks by minimum priority level."""
        return [task for task in self.available_tasks 
                if task.priority.value >= min_priority.value]
    
    def set_scheduling_rule(self, rule_name: str, rule_func: callable) -> None:
        """Add a custom scheduling rule."""
        self.scheduling_rules[rule_name] = rule_func
    
    def set_priority_weight(self, priority: Priority, weight: int) -> None:
        """Set the weight for a priority level."""
        self.priority_weights[priority] = weight
    
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
        schedule = Schedule(date=date)
        
        # Get all applicable tasks for all pets
        all_applicable_tasks = []
        for pet in self.owner.pets:
            pet_tasks = self._filter_applicable_tasks(pet)
            for task in pet_tasks:
                all_applicable_tasks.append((task, pet))
        
        # Sort by priority and overdue status
        sorted_tasks = self._sort_tasks_by_priority([task for task, _ in all_applicable_tasks])
        
        # Track completed recurring tasks for auto-generation
        completed_recurring_tasks = []
        
        # Try to schedule each task
        for task in sorted_tasks:
            # Find which pet this task belongs to
            applicable_pet = None
            for task_pet_pair in all_applicable_tasks:
                if task_pet_pair[0] == task:
                    applicable_pet = task_pet_pair[1]
                    break
            
            if applicable_pet is None:
                continue
            
            # Find optimal time slot
            time_slot = self.find_optimal_time_slot(task, constraints, schedule)
            
            if time_slot:
                reason = self._generate_scheduling_reason(task, applicable_pet, time_slot)
                scheduled_task = ScheduledTask(task, time_slot, reason)
                schedule.add_scheduled_task(scheduled_task)
                
                # Use our custom sorting algorithm to maintain order
                schedule.scheduled_tasks = self.sort_by_time(schedule.scheduled_tasks)
                
                # Stop if we've reached time limit
                if schedule.get_total_duration() >= constraints.get_remaining_time(0):
                    break
        
        return schedule
    
    def complete_task_and_handle_recurring(self, scheduled_task: ScheduledTask) -> Optional[Task]:
        """Complete a task and automatically create next instance if recurring."""
        scheduled_task.set_status(TaskStatus.COMPLETED)
        
        # Get the next recurring instance if applicable
        next_task = scheduled_task.get_next_recurring_task()
        if next_task:
            # Automatically add the new recurring task to available tasks
            self.add_task(next_task)
            return next_task
        
        return None
    
    def score_task(self, task: Task, pet: Pet, time_slot: datetime) -> float:
        """
        Calculate a score for scheduling a task at a given time.
        
        Higher scores indicate better scheduling choices.
        """
        score = 0.0
        
        # Base priority score
        score += self.priority_weights.get(task.priority, task.priority.value)
        
        # Overdue bonus
        if task.is_overdue():
            score += 5.0
        
        # Time preference bonus
        preferred_time = pet.preferences.get(f"{task.category.value}_time")
        if preferred_time:
            if self._time_matches_preference(time_slot, preferred_time):
                score += 2.0
        
        # Energy level matching
        pet_energy = pet.preferences.get("energy_level", EnergyLevel.MODERATE.value)
        task_energy_req = task.requirements.get("min_energy_level")
        if task_energy_req and pet_energy == task_energy_req:
            score += 1.0
        
        return score
    
    def find_optimal_time_slot(
        self, 
        task: Task, 
        constraints: SchedulingConstraints,
        current_schedule: Schedule = None
    ) -> Optional[datetime]:
        """Find the best time slot for a task given constraints."""
        if current_schedule is None:
            current_schedule = Schedule(datetime.now())
        
        # Generate potential time slots (15-minute intervals)
        potential_slots = []
        current_time = constraints.start_time
        
        while current_time + timedelta(minutes=task.duration_minutes) <= constraints.end_time:
            potential_slots.append(current_time)
            current_time += timedelta(minutes=15)
        
        best_slot = None
        best_score = -1
        
        for slot in potential_slots:
            if self._check_time_constraints(task, slot, constraints, current_schedule):
                # Score this slot (assuming first pet for now - could be improved)
                if self.owner.pets:
                    score = self.score_task(task, self.owner.pets[0], slot)
                    if score > best_score:
                        best_score = score
                        best_slot = slot
        
        return best_slot
    
    def validate_schedule(self, schedule: Schedule) -> bool:
        """Validate that a schedule meets all constraints."""
        # Check for conflicts
        if schedule.has_conflicts():
            return False
        
        # Check if all tasks are applicable to their pets
        for scheduled_task in schedule.scheduled_tasks:
            task = scheduled_task.task
            # Check if task is applicable to at least one pet
            applicable = any(task.is_applicable_for_pet(pet) for pet in self.owner.pets)
            if not applicable:
                return False
        
        return True
    
    def detect_pet_conflicts(self, schedule: Schedule) -> dict[str, list[dict]]:
        """Detect scheduling conflicts for each individual pet."""
        pet_conflicts = {}
        
        for pet in self.owner.pets:
            conflicts = []
            pet_tasks = []
            
            # Find all tasks scheduled for this pet
            for scheduled_task in schedule.scheduled_tasks:
                if scheduled_task.task.is_applicable_for_pet(pet):
                    pet_tasks.append(scheduled_task)
            
            # Sort pet tasks by time for conflict detection
            pet_tasks_sorted = self.sort_by_time(pet_tasks)
            
            # Check for overlaps in this pet's schedule
            for i in range(len(pet_tasks_sorted) - 1):
                current = pet_tasks_sorted[i]
                next_task = pet_tasks_sorted[i + 1]
                
                if current.get_end_time() > next_task.scheduled_time:
                    overlap_minutes = int((current.get_end_time() - next_task.scheduled_time).total_seconds() / 60)
                    conflicts.append({
                        'task1': current.task.title,
                        'task2': next_task.task.title,
                        'overlap_start': next_task.scheduled_time,
                        'overlap_end': current.get_end_time(),
                        'overlap_duration_minutes': overlap_minutes
                    })
            
            if conflicts:
                pet_conflicts[pet.name] = conflicts
        
        return pet_conflicts
    
    def detect_resource_conflicts(self, schedule: Schedule) -> list[dict]:
        """Detect if multiple pets need the same resource (owner) at the same time."""
        resource_conflicts = []
        sorted_tasks = schedule.get_scheduled_tasks()
        
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task1 = sorted_tasks[i]
                task2 = sorted_tasks[j]
                
                # Check if tasks overlap in time
                if schedule._tasks_overlap(task1, task2):
                    # Find which pets each task applies to
                    pets1 = [pet.name for pet in self.owner.pets if task1.task.is_applicable_for_pet(pet)]
                    pets2 = [pet.name for pet in self.owner.pets if task2.task.is_applicable_for_pet(pet)]
                    
                    # If different pets need attention at the same time, it's a resource conflict
                    if not set(pets1).intersection(set(pets2)):
                        resource_conflicts.append({
                            'task1': task1.task.title,
                            'task2': task2.task.title,
                            'pets1': pets1,
                            'pets2': pets2,
                            'conflict_time': max(task1.scheduled_time, task2.scheduled_time),
                            'conflict_type': 'owner_availability'
                        })
        
        return resource_conflicts
    
    def explain_scheduling_decisions(self, schedule: Schedule) -> dict:
        """
        Return explanations for why each task was scheduled when it was.
        
        Returns:
            Dict mapping task titles to explanation strings
        """
        explanations = {}
        
        for scheduled_task in schedule.scheduled_tasks:
            task = scheduled_task.task
            explanations[task.title] = scheduled_task.reason
        
        return explanations
    
    # ---- Private Methods ----
    
    def _filter_applicable_tasks(self, pet: Pet) -> list[Task]:
        """Filter tasks that are applicable for the given pet."""
        applicable_tasks = []
        for task in self.available_tasks:
            if task.is_applicable_for_pet(pet):
                applicable_tasks.append(task)
        return applicable_tasks
    
    def _sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority score (highest first)."""
        return sorted(tasks, key=lambda t: t.get_priority_score(), reverse=True)
    
    def _check_time_constraints(
        self, 
        task: Task, 
        time_slot: datetime, 
        constraints: SchedulingConstraints,
        current_schedule: Schedule = None
    ) -> bool:
        """Check if a task can be scheduled at the given time slot."""
        # Check if time is allowed for this category
        if not constraints.is_time_allowed(time_slot, task.category):
            return False
        
        # Check if task would end before constraint end time
        task_end = time_slot + timedelta(minutes=task.duration_minutes)
        if task_end > constraints.end_time:
            return False
        
        # Check for conflicts with already scheduled tasks
        if current_schedule:
            for scheduled_task in current_schedule.scheduled_tasks:
                existing_start = scheduled_task.scheduled_time
                existing_end = scheduled_task.get_end_time()
                
                # Check overlap
                if not (task_end <= existing_start or time_slot >= existing_end):
                    if not constraints.allow_overlap:
                        return False
        
        return True
    
    def _generate_scheduling_reason(self, task: Task, pet: Pet, time_slot: datetime) -> str:
        """Generate a human-readable reason for scheduling a task at a specific time."""
        reasons = []
        
        if task.priority == Priority.CRITICAL:
            reasons.append("Critical priority")
        elif task.priority == Priority.HIGH:
            reasons.append("High priority")
        
        if task.is_overdue():
            reasons.append("Overdue task")
        
        # Check time preferences
        preferred_time = pet.preferences.get(f"{task.category.value}_time")
        if preferred_time and self._time_matches_preference(time_slot, preferred_time):
            reasons.append(f"Matches {pet.name}'s preferred {preferred_time} time")
        
        # Energy matching
        pet_energy = pet.preferences.get("energy_level")
        if pet_energy:
            reasons.append(f"{pet.name} has {pet_energy} energy level")
        
        if not reasons:
            reasons.append("Best available time slot")
        
        return ", ".join(reasons)
    
    def _time_matches_preference(self, time_slot: datetime, preference: str) -> bool:
        """Check if time slot matches a time preference."""
        hour = time_slot.hour
        
        time_ranges = {
            "early_morning": (6, 8),
            "morning": (8, 10),
            "late_morning": (10, 12),
            "afternoon": (12, 16),
            "evening": (16, 19),
            "night": (19, 22)
        }
        
        if preference in time_ranges:
            start, end = time_ranges[preference]
            return start <= hour < end
        
        return True


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    print("=== PawPal+ Fully Implemented System Demo ===\\n")
    
    # Create owner
    owner = Owner(name="Jordan", available_time_minutes=240)  # 4 hours available
    
    # Create pets with preferences and conditions
    dog = Pet(name="Mochi", species="dog", age=3, breed="Golden Retriever")
    dog.set_time_preference("walk", TimeOfDay.MORNING)
    dog.set_energy_level(EnergyLevel.HIGH)
    dog.set_activity_preference(ActivityPreference.OUTDOOR_PREFERRED)
    dog.add_medical_condition(MedicalCondition.ARTHRITIS, "mild, avoid intense exercise")
    
    cat = Pet(name="Whiskers", species="cat", age=5, breed="Maine Coon")
    cat.set_time_preference("grooming", TimeOfDay.AFTERNOON)
    cat.set_energy_level(EnergyLevel.MODERATE)
    cat.set_activity_preference(ActivityPreference.INDOOR_ONLY)
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Set owner's available time window (8 AM to 6 PM)
    today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = today.replace(hour=18)
    owner.set_time_window(today, end_time)
    
    print(f"Owner: {owner}")
    print(f"Available time: {owner.get_available_time()} minutes")
    print()
    
    # Create diverse tasks
    tasks = [
        # Dog tasks
        Task("Morning Dog Walk", 30, Priority.HIGH, TaskCategory.EXERCISE),
        Task("Feed Dog", 10, Priority.CRITICAL, TaskCategory.FEEDING),
        Task("Dog Training Session", 45, Priority.MEDIUM, TaskCategory.TRAINING),
        Task("Brush Dog", 15, Priority.LOW, TaskCategory.GROOMING),
        
        # Cat tasks  
        Task("Feed Cat", 5, Priority.CRITICAL, TaskCategory.FEEDING),
        Task("Clean Litter Box", 10, Priority.MEDIUM, TaskCategory.MAINTENANCE),
        Task("Cat Grooming", 20, Priority.MEDIUM, TaskCategory.GROOMING),
        Task("Cat Enrichment Play", 25, Priority.LOW, TaskCategory.ENRICHMENT),
        
        # General tasks
        Task("Vet Medication", 5, Priority.CRITICAL, TaskCategory.MEDICAL),
    ]
    
    # Set task requirements and make some recurring
    tasks[0].add_species_requirement("dog")  # Morning walk
    tasks[0].set_recurring(1)  # Daily
    
    tasks[1].add_species_requirement("dog")  # Feed dog
    tasks[1].set_recurring(1)  # Daily
    
    tasks[3].add_species_requirement("dog")  # Brush dog
    tasks[3].add_medical_restriction(MedicalCondition.ARTHRITIS)  # Mochi can't do this
    
    tasks[4].add_species_requirement("cat")  # Feed cat
    tasks[4].set_recurring(1)  # Daily
    
    tasks[5].add_species_requirement("cat")  # Litter box
    tasks[5].set_recurring(2)  # Every 2 days
    
    tasks[6].add_species_requirement("cat")  # Cat grooming
    
    tasks[7].add_species_requirement("cat")  # Cat play
    tasks[7].add_energy_requirement(EnergyLevel.MODERATE)
    
    # Create scheduler and add tasks
    scheduler = Scheduler(owner)
    for task in tasks:
        scheduler.add_task(task)

    print("=== Available Tasks ===")
    for task in tasks:
        print(f"  - {task}")
    print()

    # Test task filtering
    print("=== Task Applicability Test ===")
    for pet in [dog, cat]:
        applicable = scheduler._filter_applicable_tasks(pet)
        print(f"{pet.name} can do {len(applicable)} tasks:")
        for task in applicable:
            print(f"  ✓ {task.title}")
        print()

    # Create scheduling constraints
    constraints = SchedulingConstraints(
        start_time=today,
        end_time=end_time,
        max_total_duration=180  # 3 hours max
    )

    # Set some preferences
    constraints.set_time_preference(TaskCategory.FEEDING, TimeOfDay.MORNING)
    constraints.set_time_preference(TaskCategory.GROOMING, TimeOfDay.AFTERNOON)
    constraints.add_exclusion(TaskCategory.TRAINING)  # No training today

    print(f"Constraints: {constraints}")
    print()

    # Generate optimized schedule
    print("=== Generating Optimized Schedule ===")
    schedule = scheduler.generate_daily_schedule(today, constraints)

    print(f"Schedule: {schedule}")
    print(f"Total duration: {schedule.get_total_duration()} minutes")
    print(f"Has conflicts: {schedule.has_conflicts()}")
    print()

    # Display schedule details
    print("=== Schedule Details ===")
    print(schedule.get_schedule_summary())
    print()

    scheduled_tasks = schedule.get_scheduled_tasks()
    if scheduled_tasks:
        print("Scheduled Tasks:")
        for i, scheduled_task in enumerate(scheduled_tasks, 1):
            task = scheduled_task.task
            print(f"{i}. {scheduled_task}")
            print(f"   Category: {task.category.value.title()}")
            print(f"   Reason: {scheduled_task.reason}")
            print()

    # Show explanations
    explanations = scheduler.explain_scheduling_decisions(schedule)
    print("=== Scheduling Explanations ===")
    for task_title, explanation in explanations.items():
        print(f"{task_title}: {explanation}")
    print()

    # Show free time slots
    free_slots = schedule.get_free_time_slots()
    if free_slots:
        print("=== Free Time Slots ===")
        for start, end in free_slots:
            duration = int((end - start).total_seconds() / 60)
            print(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')} ({duration} min)")

    print("\n=== System Features Demonstrated ===")
    print("✓ Multi-pet scheduling with individual preferences")
    print("✓ Priority-based task ordering") 
    print("✓ Medical condition restrictions")
    print("✓ Time preference matching")
    print("✓ Constraint-based filtering")
    print("✓ Conflict detection")
    print("✓ Detailed scheduling explanations")
    print("✓ Recurring task support")
    print("\nPawPal+ is ready for Streamlit integration!")
    
    print("=== Available Tasks ===") 
    for task in tasks:
        print(f"  - {task}")
    print()
    
    # Test task filtering
    print("=== Task Applicability Test ===")
    for pet in [dog, cat]:
        applicable = scheduler._filter_applicable_tasks(pet)
        print(f"{pet.name} can do {len(applicable)} tasks:")
        for task in applicable:
            print(f"  ✓ {task.title}")
        print()
    
    # Create scheduling constraints
    constraints = SchedulingConstraints(
        start_time=today,
        end_time=end_time,
        max_total_duration=180  # 3 hours max
    )
    
    # Set some preferences
    constraints.set_time_preference(TaskCategory.FEEDING, TimeOfDay.MORNING)
    constraints.set_time_preference(TaskCategory.GROOMING, TimeOfDay.AFTERNOON)
    constraints.add_exclusion(TaskCategory.TRAINING)  # No training today
    
    print(f"Constraints: {constraints}")
    print()
    
    # Generate optimized schedule
    print("=== Generating Optimized Schedule ===")
    schedule = scheduler.generate_daily_schedule(today, constraints)
    
    print(f"Schedule: {schedule}")
    print(f"Total duration: {schedule.get_total_duration()} minutes")
    print(f"Has conflicts: {schedule.has_conflicts()}")
    print()
    
    # Display schedule details
    print("=== Schedule Details ===")
    print(schedule.get_schedule_summary())
    print()
    
    scheduled_tasks = schedule.get_scheduled_tasks()
    if scheduled_tasks:
        print("Scheduled Tasks:")
        for i, scheduled_task in enumerate(scheduled_tasks, 1):
            task = scheduled_task.task
            print(f"{i}. {scheduled_task}")
            print(f"   Category: {task.category.value.title()}")
            print(f"   Reason: {scheduled_task.reason}")
            print()
    
    # Show explanations
    explanations = scheduler.explain_scheduling_decisions(schedule)
    print("=== Scheduling Explanations ===")
    for task_title, explanation in explanations.items():
        print(f"{task_title}: {explanation}")
    print()
    
    # Show free time slots
    free_slots = schedule.get_free_time_slots()
    if free_slots:
        print("=== Free Time Slots ===")
        for start, end in free_slots:
            duration = int((end - start).total_seconds() / 60)
            print(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')} ({duration} min)")
    
    print("\n=== System Features Demonstrated ===")
    print("✓ Multi-pet scheduling with individual preferences")
    print("✓ Priority-based task ordering") 
    print("✓ Medical condition restrictions")
    print("✓ Time preference matching")
    print("✓ Constraint-based filtering")
    print("✓ Conflict detection")
    print("✓ Detailed scheduling explanations")
    print("✓ Recurring task support")
    print("\nPawPal+ is ready for Streamlit integration!")