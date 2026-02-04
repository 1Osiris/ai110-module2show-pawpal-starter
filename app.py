import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import (
    Owner, Pet, Task, Scheduler, SchedulingConstraints,
    Priority, TaskCategory, TaskStatus, TimeOfDay, EnergyLevel, 
    ActivityPreference, MedicalCondition
)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# Initialize session state
def initialize_session_state():
    """Initialize all session state objects if they don't exist."""
    if 'owner' not in st.session_state:
        st.session_state.owner = None
    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = None
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'current_schedule' not in st.session_state:
        st.session_state.current_schedule = None

initialize_session_state()

st.title("🐾 PawPal+ Pet Care Scheduler")

st.markdown(
    """
**PawPal+** intelligently schedules pet care tasks based on your pets' needs, energy levels, 
medical conditions, and time preferences. Create optimized daily schedules that keep your furry friends happy and healthy!
"""
)

# Sidebar for owner setup
with st.sidebar:
    st.header("👤 Owner Setup")
    
    owner_name = st.text_input("Owner name", value="Pet Parent")
    available_time = st.slider("Available time (hours)", 1, 12, 5)
    
    if st.button("Create/Update Owner"):
        st.session_state.owner = Owner(
            name=owner_name, 
            available_time_minutes=available_time * 60
        )
        # Reset scheduler when owner changes
        if st.session_state.owner:
            st.session_state.scheduler = Scheduler(st.session_state.owner)
        st.success(f"✅ Owner '{owner_name}' created!")
    
    if st.session_state.owner:
        st.info(f"Current owner: {st.session_state.owner.name}")
        st.info(f"Available: {st.session_state.owner.get_available_time()} minutes")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🐕 Pet Management")
    
    if st.session_state.owner is None:
        st.warning("⚠️ Please create an owner first in the sidebar!")
    else:
        # Add Pet Form
        with st.form("add_pet_form"):
            st.write("**Add New Pet**")
            pet_name = st.text_input("Pet name", value="Buddy")
            pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
            pet_age = st.number_input("Age (years)", min_value=0, max_value=25, value=3)
            pet_breed = st.text_input("Breed", value="Mixed")
            
            # Pet characteristics
            energy_level = st.selectbox("Energy Level", 
                [e.value for e in EnergyLevel], 
                index=2  # MODERATE
            )
            
            activity_pref = st.selectbox("Activity Preference",
                [a.value for a in ActivityPreference],
                index=2  # MIXED
            )
            
            # Medical conditions
            medical_conditions = st.multiselect("Medical Conditions",
                [m.value for m in MedicalCondition]
            )
            
            if st.form_submit_button("🐾 Add Pet"):
                # Create pet with characteristics
                new_pet = Pet(pet_name, pet_species, pet_age, pet_breed)
                new_pet.set_energy_level(EnergyLevel(energy_level))
                new_pet.set_activity_preference(ActivityPreference(activity_pref))
                
                # Add medical conditions
                for condition in medical_conditions:
                    new_pet.add_medical_condition(MedicalCondition(condition), "")
                
                # Add to owner
                st.session_state.owner.add_pet(new_pet)
                st.success(f"✅ Added {pet_name} to {st.session_state.owner.name}'s pets!")
                st.rerun()
        
        # Display current pets
        if st.session_state.owner and st.session_state.owner.get_pets():
            st.write("**Current Pets:**")
            for i, pet in enumerate(st.session_state.owner.get_pets()):
                with st.expander(f"🐾 {pet.name} ({pet.species})"):
                    st.write(f"**Age:** {pet.age} years")
                    st.write(f"**Breed:** {pet.breed}")
                    st.write(f"**Energy:** {pet.preferences.get('energy_level', 'unknown')}")
                    st.write(f"**Activity Style:** {pet.preferences.get('activity_style', 'unknown')}")
                    
                    conditions = list(pet.get_medical_conditions().keys())
                    if conditions:
                        st.write(f"**Medical:** {', '.join(conditions)}")
                    
                    if st.button(f"Remove {pet.name}", key=f"remove_pet_{i}"):
                        st.session_state.owner.remove_pet(pet)
                        st.success(f"Removed {pet.name}")
                        st.rerun()

with col2:
    st.subheader("📋 Task Management")
    
    if st.session_state.owner is None:
        st.warning("⚠️ Please create an owner first!")
    elif not st.session_state.owner.get_pets():
        st.warning("⚠️ Please add at least one pet first!")
    else:
        # Add Task Form
        with st.form("add_task_form"):
            st.write("**Add New Task**")
            task_title = st.text_input("Task title", value="Morning walk")
            task_duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, value=30)
            
            task_priority = st.selectbox("Priority", 
                [p.name for p in Priority],
                index=1  # MEDIUM
            )
            
            task_category = st.selectbox("Category",
                [c.value for c in TaskCategory],
                index=1  # EXERCISE
            )
            
            # Task requirements
            species_req = st.selectbox("Required Species", 
                ["any"] + [pet.species for pet in st.session_state.owner.get_pets()]
            )
            
            energy_req = st.selectbox("Minimum Energy Level Required",
                ["none"] + [e.value for e in EnergyLevel],
                index=0
            )
            
            is_recurring = st.checkbox("Recurring task")
            frequency_days = 1
            if is_recurring:
                frequency_days = st.number_input("Every N days", min_value=1, max_value=30, value=1)
            
            if st.form_submit_button("📋 Add Task"):
                # Create task
                new_task = Task(
                    title=task_title,
                    duration_minutes=int(task_duration),
                    priority=Priority[task_priority],
                    category=TaskCategory(task_category)
                )
                
                # Set requirements
                if species_req != "any":
                    new_task.add_species_requirement(species_req)
                
                if energy_req != "none":
                    new_task.add_energy_requirement(EnergyLevel(energy_req))
                
                if is_recurring:
                    new_task.set_recurring(frequency_days)
                
                # Add to scheduler
                if not st.session_state.scheduler:
                    st.session_state.scheduler = Scheduler(st.session_state.owner)
                
                st.session_state.scheduler.add_task(new_task)
                st.success(f"✅ Added task '{task_title}'!")
                st.rerun()
        
        # Display current tasks
        if st.session_state.scheduler and st.session_state.scheduler.available_tasks:
            st.write("**Current Tasks:**")
            for i, task in enumerate(st.session_state.scheduler.available_tasks):
                with st.expander(f"📋 {task.title} ({task.duration_minutes} min)"):
                    st.write(f"**Priority:** {task.priority.name}")
                    st.write(f"**Category:** {task.category.value}")
                    
                    if "species" in task.requirements:
                        st.write(f"**Species:** {task.requirements['species']}")
                    
                    if task.is_recurring:
                        st.write(f"**Recurring:** Every {task.frequency_days} day(s)")
                    
                    if st.button(f"Remove Task", key=f"remove_task_{i}"):
                        st.session_state.scheduler.remove_task(task)
                        st.success(f"Removed {task.title}")
                        st.rerun()

st.divider()

st.subheader("🗓️ Schedule Generation")

if not st.session_state.scheduler or not st.session_state.scheduler.available_tasks:
    st.warning("⚠️ Please add some tasks first!")
elif not st.session_state.owner or not st.session_state.owner.get_pets():
    st.warning("⚠️ Please add an owner and pets first!")
else:
    # Schedule configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        schedule_date = st.date_input("Schedule Date", datetime.now().date())
        start_hour = st.selectbox("Start Time", list(range(5, 12)), index=2)  # 7 AM
        
    with col2:
        end_hour = st.selectbox("End Time", list(range(12, 24)), index=8)  # 8 PM
        max_duration = st.slider("Max Total Time (hours)", 1, 12, 4)
        
    with col3:
        st.write("**Time Preferences:**")
        feeding_time = st.selectbox("Feeding", [t.value for t in TimeOfDay], index=1)
        exercise_time = st.selectbox("Exercise", [t.value for t in TimeOfDay], index=1)
        grooming_time = st.selectbox("Grooming", [t.value for t in TimeOfDay], index=3)
    
    if st.button("🚀 Generate Optimized Schedule", type="primary"):
        # Create scheduling constraints
        start_time = datetime.combine(schedule_date, datetime.min.time().replace(hour=start_hour))
        end_time = datetime.combine(schedule_date, datetime.min.time().replace(hour=end_hour))
        
        constraints = SchedulingConstraints(
            start_time=start_time,
            end_time=end_time,
            max_total_duration=max_duration * 60  # Convert to minutes
        )
        
        # Set time preferences
        constraints.set_time_preference(TaskCategory.FEEDING, TimeOfDay(feeding_time))
        constraints.set_time_preference(TaskCategory.EXERCISE, TimeOfDay(exercise_time))
        constraints.set_time_preference(TaskCategory.GROOMING, TimeOfDay(grooming_time))
        
        # Generate schedule
        schedule = st.session_state.scheduler.generate_daily_schedule(start_time, constraints)
        st.session_state.current_schedule = schedule
        
        # Display results
        if schedule.scheduled_tasks:
            st.success(f"✅ Generated schedule with {len(schedule.scheduled_tasks)} tasks!")
            
            # Schedule overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", len(schedule.scheduled_tasks))
            with col2:
                st.metric("Total Time", f"{schedule.get_total_duration()//60}h {schedule.get_total_duration()%60}m")
            with col3:
                conflict_status = "❌ Yes" if schedule.has_conflicts() else "✅ None"
                st.metric("Conflicts", conflict_status)
            
            # Detailed schedule
            st.subheader("📅 Today's Schedule")
            
            # Initialize task completion tracking
            if 'completed_tasks' not in st.session_state:
                st.session_state.completed_tasks = {}
            
            for i, scheduled_task in enumerate(schedule.get_scheduled_tasks(), 1):
                task = scheduled_task.task
                start_time = scheduled_task.scheduled_time
                end_time = scheduled_task.get_end_time()
                
                # Create unique task key
                task_key = f"{task.title}_{start_time.strftime('%H%M')}_{i}"
                
                # Find applicable pet
                applicable_pets = [pet.name for pet in st.session_state.owner.get_pets() 
                                 if task.is_applicable_for_pet(pet)]
                
                # Check if task is completed
                is_completed = st.session_state.completed_tasks.get(task_key, False)
                
                # Show completion status in title
                status_icon = "✅" if is_completed else "⏳"
                status_text = "COMPLETED" if is_completed else "PENDING"
                
                with st.expander(
                    f"{status_icon} {i}. {start_time.strftime('%I:%M %p')} - {task.title} "
                    f"({task.duration_minutes} min) - {status_text}"
                ):
                    # Add completion checkbox at the top
                    col_checkbox, col_label = st.columns([1, 4])
                    with col_checkbox:
                        task_completed = st.checkbox(
                            "✅ Done", 
                            value=is_completed,
                            key=f"complete_checkbox_{task_key}"
                        )
                        # Update completion status when checkbox changes
                        if task_completed != is_completed:
                            st.session_state.completed_tasks[task_key] = task_completed
                            if task_completed:
                                st.success(f"✅ Completed: {task.title}")
                                # Handle recurring tasks
                                if task.is_recurring:
                                    st.info(f"🔄 This is a recurring task (every {task.frequency_days} days)")
                            else:
                                st.info(f"↩️ Marked as pending: {task.title}")
                    
                    with col_label:
                        if is_completed:
                            st.success("Task completed! 🎉")
                        else:
                            st.write("Check the box when you complete this task")
                    
                    st.divider()
                    
                    # Task details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Time:** {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}")
                        st.write(f"**Pet(s):** {', '.join(applicable_pets) if applicable_pets else 'Any'}")
                        st.write(f"**Category:** {task.category.value.title()}")
                    
                    with col2:
                        st.write(f"**Priority:** {task.priority.name}")
                        st.write(f"**Duration:** {task.duration_minutes} minutes")
                        if task.is_recurring:
                            st.write(f"**Recurring:** Every {task.frequency_days} day(s)")
                    
                    st.write(f"**Scheduling Reason:** {scheduled_task.reason}")
            
            # Show completion summary
            if st.session_state.completed_tasks:
                completed_count = sum(1 for completed in st.session_state.completed_tasks.values() if completed)
                total_tasks = len(schedule.scheduled_tasks)
                
                if completed_count > 0:
                    progress = completed_count / total_tasks
                    st.subheader(f"🏆 Progress: {completed_count}/{total_tasks} tasks completed")
                    st.progress(progress)
                    
                    if completed_count == total_tasks:
                        st.balloons()
                        st.success("🎉 Congratulations! All tasks completed for today!")
                    
                    # Show completed tasks
                    with st.expander("✅ Completed Tasks"):
                        completed_tasks = [key for key, completed in st.session_state.completed_tasks.items() if completed]
                        for task_key in completed_tasks:
                            task_name = task_key.split('_')[0].replace('_', ' ')
                            st.write(f"✅ {task_name}")
                    
                    # Reset button for completions
                    if st.button("🔄 Reset All Completions"):
                        st.session_state.completed_tasks = {}
                        st.success("All task completions reset!")
            
            # Free time slots
            free_slots = schedule.get_free_time_slots()
            if free_slots:
                st.subheader("🆓 Free Time Slots")
                for start, end in free_slots:
                    duration = int((end - start).total_seconds() / 60)
                    st.info(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')} ({duration} minutes)")
            
            # Schedule summary
            st.subheader("📊 Schedule Analysis")
            
            # Show detailed conflict analysis
            if schedule.has_conflicts():
                st.error("⚠️ **Schedule Conflicts Detected**")
                
                with st.expander("🔍 Detailed Conflict Analysis", expanded=True):
                    # Show detailed conflicts
                    detailed_conflicts = schedule.get_detailed_conflicts()
                    if detailed_conflicts:
                        st.write("**Time Overlap Conflicts:**")
                        for i, conflict in enumerate(detailed_conflicts, 1):
                            st.write(f"{i}. **{conflict['task1'].task.title}** vs **{conflict['task2'].task.title}**")
                            st.write(f"   Overlap: {conflict['overlap_start'].strftime('%I:%M %p')} - {conflict['overlap_end'].strftime('%I:%M %p')}")
                    
                    # Show pet-specific conflicts
                    pet_conflicts = st.session_state.scheduler.detect_pet_conflicts(schedule)
                    if pet_conflicts:
                        st.write("**Pet-Specific Conflicts:**")
                        for pet_name, conflicts in pet_conflicts.items():
                            st.write(f"🐾 **{pet_name}:**")
                            for conflict in conflicts:
                                st.write(f"   • {conflict['task1']} → {conflict['task2']} (overlap: {conflict['overlap_duration_minutes']} min)")
                    
                    # Show resource conflicts
                    resource_conflicts = st.session_state.scheduler.detect_resource_conflicts(schedule)
                    if resource_conflicts:
                        st.write("**Owner Availability Conflicts:**")
                        for conflict in resource_conflicts:
                            st.write(f"   • **{conflict['task1']}** (for {', '.join(conflict['pets1'])}) vs **{conflict['task2']}** (for {', '.join(conflict['pets2'])})")
                            st.write(f"     Conflict time: {conflict['conflict_time'].strftime('%I:%M %p')}")
            
            # Task filtering and sorting demonstration
            with st.expander("🔧 Advanced Task Analysis"):
                if st.session_state.owner and st.session_state.owner.get_pets():
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Filter Tasks by Pet:**")
                        selected_pet_name = st.selectbox("Select Pet", 
                            [pet.name for pet in st.session_state.owner.get_pets()],
                            key="filter_pet"
                        )
                        
                        if selected_pet_name:
                            selected_pet = next(pet for pet in st.session_state.owner.get_pets() if pet.name == selected_pet_name)
                            applicable_tasks = st.session_state.scheduler.filter_tasks_by_pet(selected_pet)
                            st.write(f"Tasks applicable to {selected_pet_name}:")
                            for task in applicable_tasks:
                                st.write(f"   • {task.title} ({task.category.value}, {task.priority.name})")
                    
                    with col2:
                        st.write("**Filter by Category/Priority:**")
                        filter_category = st.selectbox("Category", 
                            ["All"] + [c.value for c in TaskCategory],
                            key="filter_category"
                        )
                        filter_priority = st.selectbox("Minimum Priority",
                            [p.name for p in Priority],
                            key="filter_priority"
                        )
                        
                        if filter_category != "All":
                            category_tasks = st.session_state.scheduler.filter_tasks_by_category(TaskCategory(filter_category))
                            st.write(f"**{filter_category.title()} tasks:**")
                            for task in category_tasks:
                                st.write(f"   • {task.title}")
                        
                        priority_tasks = st.session_state.scheduler.filter_tasks_by_priority(Priority[filter_priority])
                        st.write(f"**{filter_priority}+ priority tasks:**")
                        for task in priority_tasks:
                            st.write(f"   • {task.title} ({task.priority.name})")
                
                # Show sorting demonstration
                st.write("**Sorting Algorithm Demo:**")
                if schedule.scheduled_tasks:
                    st.write("Tasks sorted by time (using merge sort algorithm):")
                    sorted_tasks = st.session_state.scheduler.sort_by_time(schedule.scheduled_tasks)
                    for i, task in enumerate(sorted_tasks, 1):
                        st.write(f"{i}. {task.scheduled_time.strftime('%I:%M %p')} - {task.task.title}")
            
            # Recurring task management
            with st.expander("🔄 Recurring Task Management"):
                st.write("**Complete Tasks and Auto-Generate Next Instance:**")
                
                if schedule.scheduled_tasks:
                    # Create a unique key for tracking completed tasks
                    if 'completed_tasks' not in st.session_state:
                        st.session_state.completed_tasks = set()
                    
                    for i, scheduled_task in enumerate(schedule.scheduled_tasks):
                        if scheduled_task.task.is_recurring:
                            task_id = f"{scheduled_task.task.title}_{i}"
                            
                            # Check if this specific task instance is already completed
                            is_completed = (task_id in st.session_state.completed_tasks or 
                                          scheduled_task.status == TaskStatus.COMPLETED)
                            
                            if not is_completed:
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.write(f"🔄 **{scheduled_task.task.title}** - Every {scheduled_task.task.frequency_days} day(s)")
                                    if scheduled_task.task.last_completed:
                                        st.caption(f"Last completed: {scheduled_task.task.last_completed.strftime('%m/%d/%Y at %I:%M %p')}")
                                    else:
                                        st.caption("Never completed")
                                
                                with col2:
                                    if st.button("✅ Complete", key=f"complete_btn_{task_id}"):
                                        # Complete the task without causing full rerun
                                        scheduled_task.set_status(TaskStatus.COMPLETED)
                                        
                                        # Create next recurring instance
                                        next_task = scheduled_task.task._create_next_recurring_instance()
                                        if next_task:
                                            st.session_state.scheduler.add_task(next_task)
                                        
                                        # Mark this task as completed in session state
                                        st.session_state.completed_tasks.add(task_id)
                                        
                                        # Show success message
                                        st.success(f"✅ {scheduled_task.task.title} completed!")
                                        if next_task:
                                            st.info(f"🔄 Next instance created for {next_task.frequency_days} days from now")
                            else:
                                st.write(f"✅ **{scheduled_task.task.title}** - Completed")
                                st.caption("Task has been marked as complete")
                
                # Show all recurring tasks status (including newly created ones)
                recurring_tasks = [task for task in st.session_state.scheduler.available_tasks if task.is_recurring]
                if recurring_tasks:
                    st.write("**All Recurring Tasks Status:**")
                    for task in recurring_tasks:
                        status = "⚠️ Overdue" if task.is_overdue() else "✅ On Schedule"
                        last_completed = task.last_completed.strftime("%m/%d/%Y at %I:%M %p") if task.last_completed else "❌ Never"
                        st.write(f"   • **{task.title}** - Every {task.frequency_days} day(s)")
                        st.write(f"     Status: {status} | Last completed: {last_completed}")
            
            explanations = st.session_state.scheduler.explain_scheduling_decisions(schedule)
            
            with st.expander("Detailed Explanations"):
                for task_title, explanation in explanations.items():
                    st.write(f"**{task_title}:** {explanation}")
        
        else:
            st.error("❌ No tasks could be scheduled with the current constraints. Try adjusting the time window or reducing task requirements.")

# Reset buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Reset All Data"):
        st.session_state.clear()
        st.success("All data cleared! Please refresh the page.")

with col2:
    if st.button("🔄 Reset Task Completions"):
        if 'completed_tasks' in st.session_state:
            st.session_state.completed_tasks.clear()
        st.success("Task completion status reset!")
