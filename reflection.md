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
