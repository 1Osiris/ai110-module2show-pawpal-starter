#!/usr/bin/env python3
"""
PawPal+ Main Demo
Demonstrates the pet care scheduling system with multiple pets and tasks.
"""

from datetime import datetime, timedelta
from pawpal_system import (
    Owner, Pet, Task, Scheduler, SchedulingConstraints,
    Priority, TaskCategory, TimeOfDay, EnergyLevel, 
    ActivityPreference, MedicalCondition
)

def main():
    print("🐾 PawPal+ Daily Schedule Generator 🐾")
    print("=" * 50)
    
    # Create Owner
    owner = Owner(name="Alex", available_time_minutes=300)  # 5 hours available
    
    # Create Pets with different characteristics
    # Pet 1: High-energy dog
    dog = Pet(name="Buddy", species="dog", age=2, breed="Border Collie")
    dog.set_energy_level(EnergyLevel.VERY_HIGH)
    dog.set_time_preference("walk", TimeOfDay.MORNING)
    dog.set_activity_preference(ActivityPreference.OUTDOOR_PREFERRED)
    
    # Pet 2: Senior cat with medical needs
    cat = Pet(name="Luna", species="cat", age=12, breed="Persian")
    cat.set_energy_level(EnergyLevel.LOW)
    cat.set_time_preference("grooming", TimeOfDay.AFTERNOON)
    cat.set_activity_preference(ActivityPreference.INDOOR_ONLY)
    cat.add_medical_condition(MedicalCondition.ARTHRITIS, "needs gentle handling")
    cat.add_medical_condition(MedicalCondition.SENIOR_MOBILITY, "limited movement")
    
    # Pet 3: Young playful rabbit
    rabbit = Pet(name="Cocoa", species="rabbit", age=1, breed="Holland Lop")
    rabbit.set_energy_level(EnergyLevel.HIGH)
    rabbit.set_time_preference("play", TimeOfDay.EVENING)
    rabbit.set_activity_preference(ActivityPreference.MIXED)
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(rabbit)
    
    print(f"Owner: {owner}")
    print(f"Available Time: {owner.get_available_time()} minutes")
    print()
    
    print("Pets:")
    for pet in owner.get_pets():
        print(f"  • {pet}")
        conditions = list(pet.get_medical_conditions().keys())
        if conditions:
            print(f"    Medical conditions: {', '.join(conditions)}")
        energy = pet.preferences.get('energy_level', 'unknown')
        print(f"    Energy level: {energy}")
    print()
    
    # Create diverse tasks with different priorities and times
    tasks = [
        # Dog tasks (morning preference)
        Task("Morning Dog Walk", 45, Priority.HIGH, TaskCategory.EXERCISE),
        Task("Feed Buddy", 10, Priority.CRITICAL, TaskCategory.FEEDING),
        Task("Dog Training Session", 30, Priority.MEDIUM, TaskCategory.TRAINING),
        Task("Brush Dog Fur", 20, Priority.LOW, TaskCategory.GROOMING),
        
        # Cat tasks (afternoon/gentle care)
        Task("Feed Luna", 5, Priority.CRITICAL, TaskCategory.FEEDING),
        Task("Gentle Cat Grooming", 25, Priority.HIGH, TaskCategory.GROOMING),
        Task("Senior Cat Medication", 5, Priority.CRITICAL, TaskCategory.MEDICAL),
        Task("Litter Box Cleaning", 10, Priority.MEDIUM, TaskCategory.MAINTENANCE),
        
        # Rabbit tasks (evening play)
        Task("Feed Cocoa", 8, Priority.CRITICAL, TaskCategory.FEEDING),
        Task("Rabbit Playtime", 35, Priority.MEDIUM, TaskCategory.ENRICHMENT),
        Task("Clean Rabbit Cage", 15, Priority.MEDIUM, TaskCategory.MAINTENANCE),
        Task("Rabbit Health Check", 10, Priority.HIGH, TaskCategory.MEDICAL),
    ]
    
    # Configure task requirements and recurring schedules
    # Dog tasks
    tasks[0].add_species_requirement("dog")  # Morning walk
    tasks[0].set_recurring(1)  # Daily
    tasks[0].add_energy_requirement(EnergyLevel.MODERATE)
    
    tasks[1].add_species_requirement("dog")  # Feed dog
    tasks[1].set_recurring(1)  # Daily
    
    tasks[2].add_species_requirement("dog")  # Training
    tasks[2].add_energy_requirement(EnergyLevel.HIGH)
    
    tasks[3].add_species_requirement("dog")  # Brush dog
    
    # Cat tasks
    tasks[4].add_species_requirement("cat")  # Feed cat
    tasks[4].set_recurring(1)  # Daily
    
    tasks[5].add_species_requirement("cat")  # Cat grooming
    tasks[5].add_energy_requirement(EnergyLevel.LOW)  # Good for senior cats
    
    tasks[6].add_species_requirement("cat")  # Medication
    tasks[6].set_recurring(1)  # Daily
    
    tasks[7].add_species_requirement("cat")  # Litter box
    tasks[7].set_recurring(2)  # Every 2 days
    
    # Rabbit tasks
    tasks[8].add_species_requirement("rabbit")  # Feed rabbit
    tasks[8].set_recurring(1)  # Daily
    
    tasks[9].add_species_requirement("rabbit")  # Rabbit play
    tasks[9].add_energy_requirement(EnergyLevel.MODERATE)
    
    tasks[10].add_species_requirement("rabbit")  # Clean cage
    tasks[10].set_recurring(3)  # Every 3 days
    
    tasks[11].add_species_requirement("rabbit")  # Health check
    
    print("Available Tasks:")
    for i, task in enumerate(tasks, 1):
        recurring = f" (every {task.frequency_days} days)" if task.is_recurring else ""
        print(f"  {i:2d}. {task}{recurring}")
    print()
    
    # Create scheduler and add tasks
    scheduler = Scheduler(owner)
    for task in tasks:
        scheduler.add_task(task)
    
    # Set up today's schedule constraints (7 AM to 8 PM)
    today = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    end_time = today.replace(hour=20, minute=0)
    
    constraints = SchedulingConstraints(
        start_time=today,
        end_time=end_time,
        max_total_duration=240  # 4 hours max
    )
    
    # Set time preferences for optimal scheduling
    constraints.set_time_preference(TaskCategory.FEEDING, TimeOfDay.MORNING)
    constraints.set_time_preference(TaskCategory.MEDICAL, TimeOfDay.MORNING)
    constraints.set_time_preference(TaskCategory.EXERCISE, TimeOfDay.MORNING)
    constraints.set_time_preference(TaskCategory.GROOMING, TimeOfDay.AFTERNOON)
    constraints.set_time_preference(TaskCategory.ENRICHMENT, TimeOfDay.EVENING)
    
    print("Scheduling Constraints:")
    print(f"  Time window: {today.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}")
    print(f"  Max duration: {constraints.max_total_duration} minutes")
    print("  Preferred times:")
    print("    • Feeding & Medical: Morning")
    print("    • Exercise: Morning") 
    print("    • Grooming: Afternoon")
    print("    • Play/Enrichment: Evening")
    print()
    
    # Generate the optimized daily schedule
    print("🗓️  TODAY'S SCHEDULE")
    print("=" * 50)
    
    schedule = scheduler.generate_daily_schedule(today, constraints)
    
    # Display schedule overview
    print(f"Date: {schedule.date.strftime('%A, %B %d, %Y')}")
    print(f"Total tasks scheduled: {len(schedule.scheduled_tasks)}")
    print(f"Total time required: {schedule.get_total_duration()} minutes ({schedule.get_total_duration()/60:.1f} hours)")
    print(f"Schedule conflicts: {'Yes' if schedule.has_conflicts() else 'No'}")
    print()
    
    # Display detailed schedule
    if schedule.scheduled_tasks:
        print("Scheduled Tasks:")
        print("-" * 50)
        
        for i, scheduled_task in enumerate(schedule.get_scheduled_tasks(), 1):
            task = scheduled_task.task
            start_time = scheduled_task.scheduled_time
            end_time = scheduled_task.get_end_time()
            
            print(f"{i:2d}. {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')} | {task.title}")
            print(f"    Pet: {[pet.name for pet in owner.pets if task.is_applicable_for_pet(pet)][0]}")
            print(f"    Duration: {task.duration_minutes} min | Priority: {task.priority.name}")
            print(f"    Category: {task.category.value.title()}")
            print(f"    Reason: {scheduled_task.reason}")
            
            if task.is_recurring:
                print(f"    📅 Recurring: Every {task.frequency_days} day{'s' if task.frequency_days > 1 else ''}")
            
            print()
    else:
        print("No tasks could be scheduled with the current constraints.")
    
    # Show free time slots
    free_slots = schedule.get_free_time_slots()
    if free_slots:
        print("🆓 Free Time Slots:")
        print("-" * 30)
        for start, end in free_slots:
            duration = int((end - start).total_seconds() / 60)
            print(f"  {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')} ({duration} minutes)")
        print()
    
    # Summary statistics
    print("📊 Schedule Summary:")
    print("-" * 30)
    
    # Count tasks by category
    category_counts = {}
    priority_counts = {}
    
    for scheduled_task in schedule.scheduled_tasks:
        task = scheduled_task.task
        
        category = task.category.value
        category_counts[category] = category_counts.get(category, 0) + 1
        
        priority = task.priority.name
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    print("Tasks by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  • {category.title()}: {count}")
    
    print("Tasks by priority:")
    for priority, count in sorted(priority_counts.items(), key=lambda x: Priority[x[0]].value, reverse=True):
        print(f"  • {priority}: {count}")
    
    print()
    print("✅ Schedule generation complete!")
    print(f"Ready to care for {len(owner.pets)} pets with {len(schedule.scheduled_tasks)} optimized tasks!")

if __name__ == "__main__":
    main()