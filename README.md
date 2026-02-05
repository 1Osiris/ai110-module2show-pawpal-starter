# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Features

### 🐾 **Multi-Pet Management**
- **Pet Profiles**: Create detailed profiles for multiple pets (dogs, cats, birds, rabbits, etc.)
- **Individual Preferences**: Set energy levels, activity preferences, and time preferences per pet
- **Medical Conditions**: Track medical conditions that affect task scheduling (arthritis, anxiety, diabetes, etc.)
- **Breed & Age Tracking**: Store breed information and age for tailored care recommendations

### 📋 **Intelligent Task Scheduling**
- **Priority-Based Scheduling**: Tasks sorted by Critical, High, Medium, Low priority levels
- **Smart Time Allocation**: Optimizes task placement within available time windows
- **Constraint-Based Planning**: Respects time preferences, medical restrictions, and pet requirements
- **Conflict Detection**: Identifies and reports time overlaps, pet-specific conflicts, and resource conflicts
- **Merge Sort Algorithm**: Uses efficient sorting algorithms for time-based task organization

### 🔄 **Recurring Task Management**
- **Automatic Recurring Tasks**: Set tasks to repeat daily, weekly, or custom intervals
- **Overdue Task Detection**: Identifies and prioritizes overdue recurring tasks
- **Next Instance Creation**: Automatically generates next occurrence when tasks are completed
- **Task Completion Tracking**: Persistent tracking of completed vs. pending tasks

### 📊 **Advanced Filtering & Analysis**
- **Pet-Specific Filtering**: View tasks applicable to individual pets
- **Category Filtering**: Filter by task type (feeding, exercise, grooming, medical, etc.)
- **Priority Filtering**: Show tasks above minimum priority thresholds
- **Status Filtering**: View completed, pending, or in-progress tasks
- **Interactive Sorting**: Sort by priority, duration, category, or alphabetically

### 🧠 **Smart Scheduling Engine**
- **Scoring Algorithm**: Evaluates optimal time slots based on multiple factors
- **Time Preference Matching**: Schedules tasks during preferred times of day
- **Energy Level Compatibility**: Matches high-energy tasks with high-energy pets
- **Medical Restriction Awareness**: Automatically excludes inappropriate tasks for pets with conditions
- **Resource Conflict Resolution**: Prevents owner double-booking across multiple pets

### 📈 **Progress Tracking & Analytics**
- **Completion Progress**: Visual progress bars and completion percentages
- **Free Time Detection**: Identifies available time slots in your schedule
- **Task Distribution Analysis**: Breakdown of tasks by category and priority
- **Conflict Analysis**: Detailed reporting of scheduling conflicts with resolution suggestions
- **Schedule Explanations**: AI-generated reasons for why tasks were scheduled at specific times

### 🎯 **Interactive User Interface**
- **Drag-and-Drop Scheduling**: Easy schedule modification through Streamlit interface
- **Real-Time Updates**: Dynamic schedule updates as preferences change
- **Expandable Task Details**: Detailed task information with completion tracking
- **Professional Data Tables**: Clean, organized display of pets, tasks, and schedules
- **Status Indicators**: Color-coded priority levels and completion status

### ⚙️ **Customizable Constraints**
- **Time Windows**: Set specific start and end times for scheduling
- **Category Exclusions**: Temporarily exclude task categories from scheduling
- **Duration Limits**: Set maximum total time for daily schedules
- **Overlap Control**: Allow or prevent task time overlaps
- **Preference Overrides**: Customize time preferences for different task types

### 🧪 **Comprehensive Testing**
- **150+ Test Cases**: Extensive test coverage for all system functionality
- **Edge Case Testing**: Validates behavior with boundary conditions and unusual scenarios
- **Algorithm Validation**: Tests sorting, filtering, and scheduling algorithms
- **Integration Testing**: End-to-end validation of complete workflows
- **Confidence Rating**: 5-star reliability rating based on comprehensive testing

### 💡 **Smart Recommendations**
- **Optimal Scheduling**: AI-powered recommendations for best task timing
- **Conflict Resolution**: Intelligent suggestions for resolving scheduling conflicts
- **Free Time Utilization**: Recommendations for productive use of available time slots
- **Medical Compliance**: Automatic adjustments for pets with health conditions

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
