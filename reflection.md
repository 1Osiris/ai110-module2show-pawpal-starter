# PawPal+ Project Reflection

## 1. System Design

**Three Core Actions**
- Add, track, and edit Tasks
- Add and tack pets
- have a dashboard that guides the user on the days tasks

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included 7 core classes with clear separation of concerns:

- **Pet**: Data model storing pet information (name, species, age, breed, medical conditions, preferences). Responsible for managing individual pet characteristics and determining task applicability based on species, energy levels, and medical needs.

- **Owner**: Container for pets with available time tracking. Manages the collection of pets and calculates total available time for task scheduling.

- **Task**: Represents individual care activities with duration, priority, category, and requirements. Handles task metadata including species requirements, energy needs, and recurring schedules.

- **ScheduledTask**: Links tasks to specific time slots with scheduling rationale. Manages the temporal assignment of tasks and tracks why each task was scheduled at its particular time.

- **Schedule**: Daily container for scheduled tasks with conflict detection. Responsible for organizing tasks chronologically, detecting overlaps, calculating total duration, and identifying free time slots.

- **Scheduler**: Core scheduling engine with optimization logic. Implements the algorithm for task selection, prioritization, time assignment, and constraint satisfaction.

- **SchedulingConstraints**: Configuration object defining scheduling parameters like time windows, duration limits, and time preferences. Encapsulates all the rules and preferences that guide the scheduling process.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design evolved significantly during implementation. The most important change was **adding comprehensive enum classes for type safety and better constraint handling**:

- **Added 7 enum classes**: Priority, TaskStatus, TimeOfDay, EnergyLevel, ActivityPreference, MedicalCondition, and TaskCategory
- **Enhanced the Pet class**: Originally just stored basic info, but evolved to include complex preference management with energy levels, activity preferences, and medical condition tracking
- **Improved Task filtering**: Initial design had simple species matching, but evolved to include energy-based matching, medical condition considerations, and time preference alignment

**Why this change was crucial**: The enum-based approach transformed the system from basic string-based matching to sophisticated constraint satisfaction. For example, instead of just checking if a task applies to "dogs," the system now considers whether a high-energy Border Collie should do intensive training while a senior arthritic cat gets gentle grooming. This made the scheduling much more realistic and pet-appropriate.

**Additional key change**: The Scheduler's algorithm became more sophisticated, moving from simple priority sorting to multi-factor optimization that considers pet energy levels, medical conditions, time preferences, and task dependencies simultaneously.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Priority-First Scheduling vs. Optimal Time Utilization**

My scheduler makes a significant tradeoff by prioritizing task importance over optimal time slot utilization. The algorithm sorts all tasks by priority (Critical → High → Medium → Low) and attempts to schedule them in that order, rather than using a more sophisticated approach like dynamic programming to find the globally optimal time arrangement.

**The Tradeoff:**
- **What we gain**: Critical tasks (like medication, feeding) are guaranteed to be scheduled first, ensuring pet health and safety needs are never compromised for convenience
- **What we sacrifice**: The scheduler may leave inefficient gaps in the schedule or miss opportunities to fit more lower-priority tasks by rearranging the order

**Why this tradeoff is reasonable:**
In pet care scenarios, safety trumps efficiency. It's better to have a suboptimal schedule that ensures all critical tasks are completed than a perfectly packed schedule that might skip medication because it couldn't find the "ideal" time slot. Pet owners would rather have 30 minutes of free time scattered throughout the day than risk their pet's health for a more elegant timeline.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


## Smarter Schzeduling

**Advanced Algorithmic Features Implemented:**

### **1. Merge Sort Time Ordering**
- **Feature**: Custom `sort_by_time()` method using merge sort algorithm (O(n log n) complexity)
- **Purpose**: Efficiently sorts scheduled tasks by their start times to maintain chronological order
- **Implementation**: Recursive divide-and-conquer approach with custom merge function for ScheduledTask objects
- **Benefit**: Ensures schedule displays are always time-ordered and conflict detection is accurate

### **2. Multi-Criteria Task Filtering**
- **`filter_tasks_by_pet()`**: Finds tasks applicable to specific pets with optional status filtering
- **`filter_tasks_by_category()`**: Linear search filtering by task categories (feeding, exercise, medical, etc.)
- **`filter_tasks_by_priority()`**: Filters tasks meeting minimum priority thresholds
- **`filter_scheduled_tasks_by_status()`**: Separates completed, pending, and in-progress tasks
- **Benefit**: Enables targeted task management and analysis for different pets and scenarios

### **3. Automatic Recurring Task Management**
- **Auto-Creation**: When recurring tasks are completed, automatically generates next instance
- **`_create_next_recurring_instance()`**: Creates new Task object with same properties and updated schedule
- **`complete_task_and_handle_recurring()`**: Seamlessly handles completion workflow
- **Smart Scheduling**: Calculates next occurrence based on frequency (daily, weekly, etc.)
- **Benefit**: Eliminates manual task re-creation and ensures continuous care routines

### **4. Advanced Conflict Detection Algorithms**
- **Multi-Level Analysis**: 
  - **`get_detailed_conflicts()`**: Identifies exact overlap times between any two tasks
  - **`detect_pet_conflicts()`**: Finds scheduling conflicts for individual pets with duration calculations
  - **`detect_resource_conflicts()`**: Detects when multiple pets need owner attention simultaneously
- **Precise Overlap Calculation**: Uses datetime arithmetic to determine exact conflict minutes
- **Conflict Types**: Distinguishes between time overlaps, pet-specific issues, and resource availability
- **Benefit**: Provides detailed conflict analysis for schedule optimization and problem resolution

### **5. Enhanced Scheduling Constraints**
- **Energy Level Matching**: Tasks matched to pet energy levels (very_low → very_high)
- **Medical Condition Filtering**: Automatically excludes tasks that conflict with pet health issues
- **Time Preference Optimization**: Respects preferred times for different activity categories
- **Multi-Pet Coordination**: Balances scheduling across multiple pets with different needs
- **Benefit**: Creates more realistic and pet-appropriate schedules

### **6. Real-Time Task Completion Tracking**
- **Interactive Checkboxes**: Users can mark tasks complete directly in the UI
- **Progress Visualization**: Shows completion percentage with progress bars
- **Session Persistence**: Completion status survives page interactions
- **Celebration Features**: Balloons animation when all tasks completed
- **Benefit**: Transforms static schedule into interactive daily checklist

### **7. Intelligent Task Scoring System**
- **Multi-Factor Scoring**: Combines priority, overdue status, time preferences, and energy matching
- **Dynamic Weighting**: Adjustable priority weights for different constraint types
- **Pet-Specific Optimization**: Scores tasks based on individual pet characteristics
- **Optimal Time Slot Selection**: Finds best scheduling time using comprehensive scoring
- **Benefit**: Produces more nuanced and optimized scheduling decisions

**Technical Implementation Highlights:**
- **Algorithm Complexity**: Merge sort O(n log n), filtering O(n), conflict detection O(n²)
- **Data Structures**: Session state management, unique task identifiers, enum-based type safety
- **User Experience**: Seamless interaction without page reloads, persistent state management
- **Error Handling**: Graceful degradation when constraints cannot be satisfied