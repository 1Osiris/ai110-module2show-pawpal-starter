# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

## Testing PawPal+

### Running Tests

To run the comprehensive test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```
For a quick test run without verbose output:
```bash
python -m pytest tests/test_pawpal.py
```

### Test Coverage

The test suite includes **150+ comprehensive test cases** covering:

#### Core Data Models (Pet, Owner, Task, Schedule)
- Basic object creation and validation
- Edge cases (empty fields, boundary values, special characters)
- Data integrity and immutability checks
- Unicode and internationalization support

#### Task Management & Scheduling Logic
- Task applicability algorithms (species, medical conditions, energy levels)
- Priority scoring and overdue task handling
- Recurring task lifecycle management
- Time preference matching and constraint enforcement

#### Scheduler Engine
- Optimal time slot finding algorithms
- Conflict detection (pet conflicts, owner resource conflicts)
- Schedule validation and generation
- Custom sorting algorithms (merge sort implementation)

#### Advanced Edge Cases & Integration
- Large-scale testing (50+ pets, 200+ tasks)
- Performance stress testing with time limits
- Complex medical restriction scenarios
- Multi-pet resource contention handling
- Boundary condition testing (midnight crossing, microsecond precision)
- Error handling and graceful degradation

#### Business Logic Validation
- Energy level hierarchy enforcement
- Medical restriction compliance
- Time window and constraint adherence
- Priority vs. preference trade-off algorithms

### Confidence Level: ⭐⭐⭐⭐⭐ (5/5 Stars)

**Excellent system reliability** based on comprehensive testing that demonstrates:

✅ **Robust Core Logic**: All fundamental scheduling algorithms work correctly under normal and extreme conditions
✅ **Edge Case Handling**: System gracefully handles invalid inputs, boundary conditions, and unexpected scenarios
✅ **Performance Validated**: Successfully handles large datasets (50+ pets, 200+ tasks) within reasonable time limits
✅ **Data Integrity**: Proper validation of business rules, medical restrictions, and scheduling constraints
✅ **Integration Stability**: End-to-end workflows function correctly across all major use cases
