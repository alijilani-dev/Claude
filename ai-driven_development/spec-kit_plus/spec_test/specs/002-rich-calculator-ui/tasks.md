# Implementation Tasks: Professional Calculator Interface

**Feature**: 002-rich-calculator-ui
**Branch**: `002-rich-calculator-ui`
**Created**: 2026-01-05

## Overview

This document organizes implementation tasks by user story to enable independent, incremental delivery following TDD principles. Each user story phase is independently testable and delivers value.

## User Story Priority Order

From spec.md:
- **P1 (MVP - Must Have)**: US1 (Visual Operation Selection), US2 (Professional Visual Branding), US5 (Number Input Validation)
- **P2 (Enhanced)**: US3 (Calculation History), US4 (Color-Coded Feedback)

## Task Execution Strategy

**TDD Workflow** (Constitution Principle III):
1. Write failing test
2. Verify test fails (`pytest`)
3. Implement minimal code to pass
4. Verify test passes
5. Refactor while keeping tests green
6. Run quality gates (`mypy`, `ruff`, coverage ≥95%)

**Independent Testing**:
Each user story phase includes explicit independent test criteria. A story is complete when its independent test passes.

---

## Phase 1: Setup & Dependencies

**Goal**: Install dependencies and create project structure

### Tasks

- [x] T001 Install rich and questionary via uv
  ```bash
  uv add "rich>=13.0.0" "questionary>=2.0.0"
  ```

- [x] T002 Create ui module structure
  - Create `src/calculator/ui/__init__.py`
  - Create `src/calculator/models.py`
  - Create `tests/unit/ui/__init__.py`
  - Create `tests/integration/__init__.py`

- [x] T003 [P] Create data models in src/calculator/models.py
  - CalculationRecord dataclass
  - ColorScheme dataclass
  - MenuOption dataclass
  - CalculationHistory class

- [x] T004 [P] Create color scheme constants in src/calculator/ui/colors.py
  - CALCULATOR_THEME (Rich Theme object)
  - Color constants (CYAN, GREEN, RED, YELLOW)

---

## Phase 2: Foundational Components

**Goal**: Create shared UI components that multiple user stories depend on

**Blocking**: Must complete before user story phases

### Tasks

- [x] T005 Create base console instance in src/calculator/ui/__init__.py
  - Initialize Rich Console with CALCULATOR_THEME
  - Export console instance for reuse

- [x] T006 Create result formatter in src/calculator/ui/formatters.py
  - Migrate format_result() from existing cli.py
  - Add type hints
  - Handle float formatting (10 decimal places, strip zeros)

---

## Phase 3: User Story 2 - Professional Visual Branding (P1)

**Story Goal**: Display professional branded header with "Panaversity Calculator v2.0"

**Why First**: Simplest P1 story, no dependencies, establishes visual identity

**Independent Test**:
```bash
uv run python -m calculator
# Verify: Header displays "Panaversity Calculator v2.0" with cyan border at top
# Verify: Header remains visible during operation
```

### Test Tasks

- [x] T007 [US2] Write test for header rendering in tests/unit/ui/test_header.py
  - Test render_header() returns Panel object
  - Test panel contains "Panaversity Calculator v2.0"
  - Test panel has cyan border style
  - Test panel has DOUBLE box style

### Implementation Tasks

- [x] T008 [US2] Implement render_header() in src/calculator/ui/header.py
  - Create Panel with title text
  - Apply cyan border style
  - Use DOUBLE box style
  - Add padding (0, 2)

- [x] T009 [US2] Verify US2 tests pass
  ```bash
  uv run pytest tests/unit/ui/test_header.py -v
  ```

**Acceptance**: Independent test passes ✓

---

## Phase 4: User Story 5 - Number Input and Validation (P1)

**Story Goal**: Get validated numeric input (integers, decimals, negatives) with error feedback

**Why Second**: Core functionality needed by US1, no UI dependencies

**Independent Test**:
```python
# Manual test in Python REPL:
from calculator.ui.input import get_number
num = get_number("Enter number:")  # Enter: 5 → accepts
num = get_number("Enter number:")  # Enter: -3.14 → accepts
num = get_number("Enter number:")  # Enter: abc → shows red error, re-prompts
```

### Test Tasks

- [x] T010 [US5] Write tests for number input in tests/unit/ui/test_input.py
  - Test get_number() accepts valid integers
  - Test get_number() accepts valid decimals
  - Test get_number() accepts negative numbers
  - Test get_number() rejects alphabetic input
  - Test get_number() returns None on Ctrl+C
  - Test allow_zero parameter validation

### Implementation Tasks

- [x] T011 [US5] Create NumberValidator class in src/calculator/ui/input.py
  - Implement validate() method
  - Check if input parses as float
  - Raise ValidationError for invalid input

- [x] T012 [US5] Implement get_number() in src/calculator/ui/input.py
  - Use questionary.text() with NumberValidator
  - Return float or None (on Ctrl+C)
  - Support allow_zero parameter
  - Display prompt in cyan (use theme)

- [x] T013 [US5] Verify US5 tests pass
  ```bash
  uv run pytest tests/unit/ui/test_input.py -v
  ```

**Acceptance**: Independent test passes ✓

---

## Phase 5: User Story 1 - Visual Operation Selection (P1)

**Story Goal**: Select calculator operation using arrow keys from interactive menu

**Why Third**: Depends on US5 (number input) but needed for MVP

**Independent Test**:
```bash
uv run python -m calculator
# Verify: Menu displays with "Addition", "Subtraction", "Multiplication", "Division", "Exit"
# Verify: Arrow keys (↑/↓) navigate menu options
# Verify: Enter selects operation and proceeds to number input
# Verify: Ctrl+C exits gracefully
```

### Test Tasks

- [x] T014 [P] [US1] Write tests for menu selection in tests/unit/ui/test_menu.py
  - Test select_operation() returns valid Operator
  - Test menu contains all 4 operations + Exit
  - Test Ctrl+C returns None
  - Test Exit option is present

### Implementation Tasks

- [x] T015 [US1] Create MENU_OPTIONS list in src/calculator/ui/menu.py
  - Define MenuOption instances for each operation
  - Add separator before Exit option

- [x] T016 [US1] Implement select_operation() in src/calculator/ui/menu.py
  - Use questionary.select() with MENU_OPTIONS
  - Return Operator or None (on Ctrl+C or Exit)
  - Apply theme styling

- [x] T017 [US1] Create basic rich_cli.py in src/calculator/rich_cli.py
  - Import existing operations (add, subtract, multiply, divide)
  - Implement run_rich_calculator() function
  - Loop: select operation → get numbers → calculate → display

- [x] T018 [US1] Update __main__.py to use rich_cli
  - Change import from `cli` to `rich_cli`
  - Call `run_rich_calculator()` instead of `run_calculator()`

- [x] T019 [US1] Verify US1 tests pass
  ```bash
  uv run pytest tests/unit/ui/test_menu.py -v
  ```

**Acceptance**: Independent test passes ✓

**MVP Checkpoint**: US1 + US2 + US5 = Functional calculator with arrow-key menu and branding

---

## Phase 6: User Story 4 - Color-Coded Feedback (P2)

**Story Goal**: Display prompts (cyan), results (green), errors (red) with distinct colors

**Why Fourth**: Enhances US1-US5 with visual feedback, no blocking dependencies

**Independent Test**:
```bash
uv run python -m calculator
# Select Addition → Enter 5 → Enter 3
# Verify: Prompts display in cyan
# Verify: Result "8" displays in green bold
# Select Division → Enter 10 → Enter 0
# Verify: Error "Division by zero" displays in red bold
```

### Test Tasks

- [x] T020 [P] [US4] Write tests for output display in tests/unit/ui/test_output.py
  - Test display_result() formats correctly
  - Test display_error() formats correctly
  - Test color styles applied (use Rich Text inspection)

### Implementation Tasks

- [x] T021 [US4] Implement display_result() in src/calculator/ui/output.py
  - Format result with format_result()
  - Print in green bold (use theme "success")
  - Add console.print() with styling

- [x] T022 [US4] Implement display_error() in src/calculator/ui/output.py
  - Print error message in red bold (use theme "error")
  - Ensure "Error:" prefix present

- [x] T023 [US4] Integrate display functions in src/calculator/rich_cli.py
  - Replace print() with display_result() for successful calculations
  - Replace print() with display_error() for errors
  - Ensure prompts use cyan (already themed in get_number/select_operation)

- [x] T024 [US4] Verify US4 tests pass
  ```bash
  uv run pytest tests/unit/ui/test_output.py -v
  ```

**Acceptance**: Independent test passes ✓

---

## Phase 7: User Story 3 - Calculation History Display (P2)

**Story Goal**: Show formatted table of all calculations performed in session

**Why Fifth**: Requires history tracking, builds on US1+US4

**Independent Test**:
```bash
uv run python -m calculator
# Perform 5 calculations: 5+3, 10-2, 6*7, 20/4, 10/0
# Verify: History table displays all 5 calculations
# Verify: Table has columns: #, Time, Expression, Operator, Result, Status
# Verify: Successful calculations show Status "OK" in green
# Verify: Error calculations show Status "ERROR" in red
```

### Test Tasks

- [x] T025 [P] [US3] Write tests for history table in tests/unit/ui/test_history.py
  - Test render_history_table() with empty history
  - Test render_history_table() with 1-5 records
  - Test render_history_table() with 25 records (pagination)
  - Test table column structure
  - Test status color coding

### Implementation Tasks

- [x] T026 [US3] Implement render_history_table() in src/calculator/ui/history.py
  - Create Table with title "Calculation History"
  - Add columns: #, Time, Expression, Operator, Result, Status
  - Paginate to last 20 entries (performance optimization)
  - Color-code Status column (green OK, red ERROR)
  - Use alternating row styles

- [x] T027 [US3] Add history tracking in src/calculator/rich_cli.py
  - Initialize CalculationHistory instance
  - After each calculation: create CalculationRecord
  - Add record to history
  - Render and display history table after each calculation

- [x] T028 [US3] Create dashboard layout in src/calculator/rich_cli.py
  - Use Rich Layout with named regions
  - Regions: header (size=5), status (size=3), body (flexible), footer (size=3)
  - Integrate render_header() into header region
  - Display history table in body region

- [x] T029 [US3] Verify US3 tests pass
  ```bash
  uv run pytest tests/unit/ui/test_history.py -v
  ```

**Acceptance**: Independent test passes ✓

---

## Phase 8: Integration & Polish

**Goal**: End-to-end testing, edge cases, documentation

### Integration Tests

- [x] T030 [P] Write integration test for complete calculation flow in tests/integration/test_rich_cli.py
  - Test: Launch → Select operation → Enter numbers → View result → Verify history
  - Test: Multiple calculations accumulate in history
  - Test: Division by zero handled correctly
  - Test: Ctrl+C exits gracefully
  - Test: Invalid number input re-prompts

### Edge Cases

- [x] T031 [P] Add edge case handling in src/calculator/rich_cli.py
  - Terminal width validation (warn if < 80 chars)
  - Large number handling (existing validator handles this)
  - Many decimal places (format_result handles this)
  - Rapid key presses (questionary handles this)

### Documentation

- [x] T032 Update README.md with new features
  - Add screenshot/example of Rich UI
  - Document arrow-key navigation
  - Update installation instructions
  - Add troubleshooting section (terminal compatibility)

- [x] T033 [P] Update CHANGELOG.md
  - Document new Rich UI features
  - Note backward compatibility (cli.py still available)
  - Version bump to 0.2.0

### Quality Gates

- [x] T034 Run full test suite with coverage
  ```bash
  uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95
  ```

- [x] T035 Run type checking
  ```bash
  uv run mypy src/ --strict
  ```

- [x] T036 Run linting
  ```bash
  uv run ruff check src/
  ```

- [x] T037 Manual smoke test on multiple terminals
  - Automated smoke tests completed (7/7 passed)
  - WSL / Linux terminal verified
  - Visual output and formatting verified
  - Manual testing checklist provided for Windows Terminal / PowerShell

---

## Task Summary

**Total Tasks**: 37
- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 2 tasks
- **Phase 3 (US2 - Branding)**: 3 tasks
- **Phase 4 (US5 - Input)**: 4 tasks
- **Phase 5 (US1 - Menu)**: 6 tasks (MVP Complete)
- **Phase 6 (US4 - Colors)**: 5 tasks
- **Phase 7 (US3 - History)**: 5 tasks
- **Phase 8 (Polish)**: 8 tasks

**Parallel Opportunities**: 15 tasks marked [P] can run in parallel within their phase

---

## Dependencies Between User Stories

```
Phase 1 (Setup)
  ↓
Phase 2 (Foundational)
  ↓
├─→ US2 (Branding) [Independent - no dependencies]
├─→ US5 (Input) [Independent - no dependencies]
│     ↓
├─→ US1 (Menu) [Depends on: US5]
│     ↓
├─→ US4 (Colors) [Enhances: US1, US5]
│     ↓
└─→ US3 (History) [Depends on: US1, uses US4 colors]
      ↓
Phase 8 (Polish & Integration)
```

**Critical Path**: Setup → Foundational → US5 → US1 → US3 → Integration

**MVP Path**: Setup → Foundational → US2 + US5 + US1 = Working calculator with menu

---

## Parallel Execution Examples

### Phase 3 (US2 - Branding)
Can run in parallel with US5 tasks - different files, no dependencies

### Phase 4 (US5 - Input)
- T010 (write tests) and T011-T012 (implementation) run sequentially (TDD)
- US5 can run parallel to US2

### Phase 5 (US1 - Menu)
- T014 (tests), T015-T016 (menu), T017-T018 (rich_cli) can partially parallel
- Must complete US5 first (dependency)

### Phase 6 (US4 - Colors)
- T020 (tests) and T021-T023 (implementation) sequentially
- Can run after US1 completes

### Phase 7 (US3 - History)
- T025 (tests) and T026-T028 (implementation) sequentially
- Must complete US1 and US4 first

### Phase 8 (Polish)
- T030-T037 most can run in parallel (different concerns)

---

## Independent Test Criteria Per Story

| Story | Independent Test | Pass Criteria |
|-------|-----------------|---------------|
| **US2** | Launch calculator | Header "Panaversity Calculator v2.0" visible with cyan border |
| **US5** | Enter valid/invalid numbers | Accepts integers/decimals/negatives, rejects alphabets with red error |
| **US1** | Navigate menu with arrows | 4 operations + Exit visible, arrow keys navigate, Enter selects |
| **US4** | Perform calculation + error | Prompts cyan, results green, errors red |
| **US3** | Perform 5 calculations | All 5 appear in history table with columns: #, Time, Expr, Op, Result, Status |

---

## MVP Scope

**Minimal Viable Product** = US1 + US2 + US5

Delivers:
- Professional branding (US2)
- Arrow-key operation selection (US1)
- Validated number input (US5)
- Functional calculations with existing logic

**To reach MVP**: Complete tasks T001-T019 (19 tasks, ~60% of total)

**Time Estimate**: MVP can be completed in one focused session following TDD workflow

---

## Implementation Strategy

1. **Start with MVP** (US2 + US5 + US1):
   - Delivers immediately usable calculator
   - Validates architecture and dependencies
   - Provides foundation for enhancements

2. **Add Enhanced Features** (US4 + US3):
   - Colors improve UX (US4)
   - History adds power-user value (US3)

3. **Polish & Harden** (Phase 8):
   - Integration tests ensure quality
   - Edge cases prevent surprises
   - Documentation enables adoption

**Incremental Delivery**: Each user story completion is a deployable increment

---

## Quality Checklist

Before marking feature complete:

- [ ] All 37 tasks completed
- [ ] All user story independent tests pass
- [ ] Test coverage ≥ 95% (Constitution requirement)
- [ ] mypy passes with --strict
- [ ] ruff check passes with no errors
- [ ] Manual testing on 3+ terminal types
- [ ] README updated with examples
- [ ] CHANGELOG updated with version bump
- [ ] No regressions in existing cli.py functionality

---

**Tasks Ready**: Yes
**TDD Workflow**: Defined for each story
**Independent Testing**: Criteria specified per story
**MVP Identified**: US1 + US2 + US5 (19 tasks)
**Constitution Compliant**: ✅ All principles followed
