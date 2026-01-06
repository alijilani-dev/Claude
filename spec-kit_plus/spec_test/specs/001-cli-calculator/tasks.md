---

description: "Task list for CLI Calculator implementation"
---

# Tasks: CLI Calculator

**Input**: Design documents from `/specs/001-cli-calculator/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/calculator_api.md

**Tests**: The constitution requires TDD (Test-Driven Development). Tests MUST be written and verified to FAIL before implementing features.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize uv project with `uv init --name calculator --app` in repository root
- [X] T002 Create pyproject.toml with Python 3.11+ requirement and dependencies (pytest, pytest-cov, mypy, ruff)
- [X] T003 [P] Create src/calculator/ directory structure with __init__.py
- [X] T004 [P] Create tests/unit/ directory with __init__.py
- [X] T005 [P] Create tests/integration/ directory with __init__.py
- [X] T006 [P] Create README.md with installation instructions from quickstart.md
- [X] T007 [P] Create .gitignore for Python (\_\_pycache\_\_, .pytest_cache, .mypy_cache, .ruff_cache, uv.lock)
- [X] T008 Run `uv sync` to install dependencies and create uv.lock

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 [P] Create src/calculator/\_\_init\_\_.py with type imports (Literal, Union, dataclass)
- [X] T010 [P] Create src/calculator/operations.py stub with function signatures (add, subtract, multiply, divide) per contracts/calculator_api.md
- [X] T011 [P] Create src/calculator/validator.py stub with function signatures (parse_number, validate_operator, parse_input, ParsedInput dataclass) per contracts/calculator_api.md
- [X] T012 [P] Create src/calculator/cli.py stub with function signatures (format_result, display_result, display_error, run_calculator) per contracts/calculator_api.md
- [X] T013 Create src/\_\_main\_\_.py entry point that imports and calls run_calculator()
- [X] T014 [P] Configure ruff in pyproject.toml with line-length=100, strict rules enabled
- [X] T015 [P] Configure mypy in pyproject.toml with strict=true, no implicit Any types
- [X] T016 [P] Configure pytest in pyproject.toml with coverage settings (minimum 95%)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Arithmetic Operations (Priority: P1) 🎯 MVP

**Goal**: Implement core calculator functionality for all four arithmetic operations with integer inputs

**Independent Test**: Launch calculator, enter "5 + 3", "10 - 4", "6 * 7", "20 / 4", verify correct results displayed

### Tests for User Story 1 (TDD - MUST FAIL BEFORE IMPLEMENTATION)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [P] [US1] Create tests/unit/test_operations.py with test_add_integers, test_subtract_integers, test_multiply_integers per contracts/calculator_api.md
- [X] T018 [P] [US1] Add test_divide_integers to tests/unit/test_operations.py (valid division only, no zero division yet)
- [X] T019 [US1] Run `uv run pytest tests/unit/test_operations.py` and verify ALL tests FAIL (no implementation yet)

### Implementation for User Story 1

- [X] T020 [P] [US1] Implement add() function in src/calculator/operations.py per contract (2 lines: return a + b)
- [X] T021 [P] [US1] Implement subtract() function in src/calculator/operations.py per contract (2 lines: return a - b)
- [X] T022 [P] [US1] Implement multiply() function in src/calculator/operations.py per contract (2 lines: return a * b)
- [X] T023 [P] [US1] Implement divide() function in src/calculator/operations.py (4 lines: check b==0, return error or a/b)
- [X] T024 [US1] Run `uv run pytest tests/unit/test_operations.py` and verify ALL tests PASS
- [X] T025 [US1] Run `uv run mypy src/calculator/operations.py --strict` and verify type checking passes

**Checkpoint**: At this point, all four basic operations are implemented and tested with integers

---

## Phase 4: User Story 4 - Error Handling and Input Validation (Priority: P1)

**Goal**: Implement robust error handling for division by zero, invalid input, invalid operators, and incomplete input

**Independent Test**: Enter "5 / 0", "abc + 5", "10 $ 5", "5 +" and verify clear error messages without crashing

### Tests for User Story 4 (TDD - MUST FAIL BEFORE IMPLEMENTATION)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T026 [P] [US4] Create tests/unit/test_validator.py with test_parse_number_valid, test_parse_number_invalid per contracts/calculator_api.md
- [X] T027 [P] [US4] Add test_validate_operator_valid, test_validate_operator_invalid to tests/unit/test_validator.py
- [X] T028 [P] [US4] Add test_parse_input_valid, test_parse_input_invalid_number, test_parse_input_invalid_operator, test_parse_input_incomplete to tests/unit/test_validator.py
- [X] T029 [P] [US4] Add test_divide_by_zero to tests/unit/test_operations.py (verify error message returned)
- [X] T030 [US4] Run `uv run pytest tests/unit/test_validator.py tests/unit/test_operations.py::test_divide_by_zero` and verify ALL new tests FAIL

### Implementation for User Story 4

- [X] T031 [P] [US4] Implement parse_number() in src/calculator/validator.py (5 lines: try float(), except ValueError return error)
- [X] T032 [P] [US4] Implement validate_operator() in src/calculator/validator.py (4 lines: check in (+,-,*,/), return operator or error)
- [X] T033 [US4] Define ParsedInput dataclass in src/calculator/validator.py (frozen=True, fields: operand1, operator, operand2)
- [X] T034 [US4] Implement parse_input() in src/calculator/validator.py (15-18 lines: split, validate count, parse numbers, validate operator, return ParsedInput or error)
- [X] T035 [US4] Update divide() in src/calculator/operations.py to check for b==0 BEFORE division (already done in T023, verify error message matches spec)
- [X] T036 [US4] Run `uv run pytest tests/unit/test_validator.py` and verify ALL tests PASS
- [X] T037 [US4] Run `uv run mypy src/calculator/validator.py --strict` and verify type checking passes

**Checkpoint**: At this point, all error handling is implemented and tested - calculator handles invalid inputs gracefully

---

## Phase 5: User Story 2 - Decimal Number Handling (Priority: P2)

**Goal**: Extend calculator to handle decimal numbers with appropriate precision (up to 10 decimal places, trailing zeros removed)

**Independent Test**: Enter "5.5 + 2.3", "10.0 / 3.0", "0.1 + 0.2", "7.5 * 2.0" and verify correct decimal results

### Tests for User Story 2 (TDD - MUST FAIL BEFORE IMPLEMENTATION)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T038 [P] [US2] Add test_add_decimals, test_subtract_decimals, test_multiply_decimals, test_divide_decimals to tests/unit/test_operations.py
- [X] T039 [P] [US2] Create tests/unit/test_edge_cases.py with test_floating_point_precision (0.1 + 0.2), test_repeating_decimals (10.0 / 3.0)
- [X] T040 [P] [US2] Add test_format_result_decimals, test_format_result_trailing_zeros to tests/unit/test_edge_cases.py
- [X] T041 [US2] Run `uv run pytest tests/unit/test_operations.py -k decimal` and verify tests work with existing operations (should already pass - operations handle floats)

### Implementation for User Story 2

- [X] T042 [US2] Implement format_result() in src/calculator/cli.py (3 lines: format to .10f, rstrip('0'), rstrip('.'))
- [X] T043 [US2] Add docstring to format_result() with examples from contracts/calculator_api.md
- [X] T044 [US2] Run `uv run pytest tests/unit/test_edge_cases.py` and verify ALL tests PASS
- [X] T045 [US2] Run `uv run mypy src/calculator/cli.py --strict` and verify type checking passes
- [X] T046 [US2] Test edge case: verify format_result(0.1 + 0.2) returns "0.3" (proper rounding)

**Checkpoint**: At this point, decimal numbers are handled correctly with proper precision formatting

---

## Phase 6: User Story 3 - Negative Number Support (Priority: P2)

**Goal**: Ensure calculator correctly handles negative numbers in all four operations

**Independent Test**: Enter "-5 + 3", "10 - 15", "-6 * -7", "-20 / 4", "-8 / -2" and verify correct signed arithmetic results

### Tests for User Story 3 (TDD - MUST FAIL BEFORE IMPLEMENTATION)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T047 [P] [US3] Add test_add_negative_numbers (multiple cases) to tests/unit/test_operations.py
- [X] T048 [P] [US3] Add test_subtract_negative_numbers (multiple cases) to tests/unit/test_operations.py
- [X] T049 [P] [US3] Add test_multiply_negative_numbers (neg*neg, neg*pos) to tests/unit/test_operations.py
- [X] T050 [P] [US3] Add test_divide_negative_numbers (neg/pos, neg/neg, pos/neg) to tests/unit/test_operations.py
- [X] T051 [P] [US3] Add test_parse_number_negative to tests/unit/test_validator.py
- [X] T052 [US3] Run `uv run pytest tests/unit/test_operations.py -k negative` and verify tests pass (operations already handle negatives - verify edge cases)

### Implementation for User Story 3

- [X] T053 [US3] Verify parse_number() handles negative numbers correctly (should already work with float() - add test verification)
- [X] T054 [US3] Verify all operations handle negative operands correctly (should already work - run comprehensive test suite)
- [X] T055 [US3] Run `uv run pytest tests/unit/test_operations.py tests/unit/test_validator.py -k negative` and verify ALL tests PASS
- [X] T056 [US3] Test edge cases: -0 (verify treated as 0), very small negative numbers

**Checkpoint**: At this point, negative numbers work correctly in all operations

---

## Phase 7: CLI Integration & End-to-End Testing

**Goal**: Integrate all components into interactive CLI and verify end-to-end user workflows

**Independent Test**: Run calculator, perform multiple calculations in sequence, verify exit works

### Tests for CLI Integration (TDD - MUST FAIL BEFORE IMPLEMENTATION)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T057 [P] Create tests/integration/test_cli_workflows.py with test_basic_calculation_flow (mock input/output)
- [X] T058 [P] Add test_error_recovery_flow to tests/integration/test_cli_workflows.py (error → continue → valid input)
- [X] T059 [P] Add test_exit_command to tests/integration/test_cli_workflows.py (verify "quit" and "exit" work)
- [X] T060 Run `uv run pytest tests/integration/` and verify ALL tests FAIL

### Implementation for CLI Integration

- [X] T061 Implement display_result() in src/calculator/cli.py (2 lines: call format_result, print)
- [X] T062 [P] Implement display_error() in src/calculator/cli.py (2 lines: print error message)
- [X] T063 Implement calculate() helper in src/calculator/cli.py (10 lines: match operator, call operation functions)
- [X] T064 Implement run_calculator() main loop in src/calculator/cli.py (15-18 lines: welcome, loop, input, parse, calculate, display, exit)
- [X] T065 Add welcome message and exit message to run_calculator()
- [X] T066 Run `uv run pytest tests/integration/` and verify ALL tests PASS
- [X] T067 Run `uv run mypy src/calculator/ --strict` and verify entire package type checks
- [X] T068 Manual test: Run `uv run python -m calculator` and verify interactive mode works end-to-end

**Checkpoint**: At this point, full CLI calculator is functional and all user stories are complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks, documentation, and validation

- [X] T069 [P] Run `uv run pytest --cov=src/calculator --cov-report=term-missing` and verify ≥95% coverage
- [X] T070 [P] Run `uv run mypy src/ --strict` and verify no type errors
- [X] T071 [P] Run `uv run ruff check src/` and verify no linting errors
- [X] T072 [P] Run `uv run ruff format src/` to format code
- [X] T073 [P] Verify all functions are <20 lines (constitution compliance check)
- [X] T074 [P] Create tests/unit/test_overflow.py with test_very_large_numbers, test_very_small_numbers per constitution edge case requirements
- [X] T075 [P] Update README.md with complete usage examples from quickstart.md
- [X] T076 Run complete test suite: `uv run pytest -v` and verify 100% pass rate
- [X] T077 Validate quickstart.md instructions by following them end-to-end
- [X] T078 [P] Add type hints to all test files for consistency
- [X] T079 Final validation: Run all quality gates (pytest, mypy strict, ruff, coverage ≥95%)
- [X] T080 Create CHANGELOG.md with v1.0.0 initial release notes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - US4 (Phase 4): Can start after Foundational - Builds on US1 operations but independently testable
  - US2 (Phase 5): Can start after Foundational - Extends operations with decimals
  - US3 (Phase 6): Can start after Foundational - Tests negative number handling (should already work)
- **CLI Integration (Phase 7)**: Depends on US1 and US4 completion (core operations + error handling)
- **Polish (Phase 8)**: Depends on all user stories and CLI integration being complete

### User Story Dependencies

- **User Story 1 (P1 - Basic Operations)**: No dependencies - Can start after Foundational (Phase 2)
- **User Story 4 (P1 - Error Handling)**: Minimal dependency on US1 (uses divide function); Can start in parallel with US1
- **User Story 2 (P2 - Decimals)**: No dependencies (uses existing operations); Can start in parallel after Foundational
- **User Story 3 (P2 - Negatives)**: No dependencies (tests existing operations); Can start in parallel after Foundational

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Implementation tasks follow: operations → validation → CLI → integration
- Core implementation before edge cases
- Story complete before moving to next priority

### Parallel Opportunities

- **All Setup tasks** (T003-T007) can run in parallel
- **All Foundational stubs** (T009-T012, T014-T016) can run in parallel
- **Once Foundational completes**, all user story test-writing phases can start in parallel:
  - T017-T019 (US1 tests)
  - T026-T030 (US4 tests)
  - T038-T041 (US2 tests)
  - T047-T052 (US3 tests)
- **Within each story**, tasks marked [P] can run in parallel
- **Different user stories** can be worked on in parallel by different team members after Foundational phase

---

## Parallel Example: After Foundational Phase

```bash
# Launch all test-writing tasks in parallel (Phase 3-6):
Task T017-T019: "Write US1 tests for basic operations"
Task T026-T030: "Write US4 tests for error handling"
Task T038-T041: "Write US2 tests for decimals"
Task T047-T052: "Write US3 tests for negatives"

# Then implement in parallel:
Task T020-T023: "Implement US1 operations"
Task T031-T034: "Implement US4 validation"
Task T042-T043: "Implement US2 formatting"
Task T053-T054: "Verify US3 negative handling"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 4 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T016)
3. Complete Phase 3: User Story 1 - Basic Operations (T017-T025)
4. Complete Phase 4: User Story 4 - Error Handling (T026-T037)
5. Complete Phase 7: CLI Integration (T057-T068)
6. **STOP and VALIDATE**: Test MVP (basic operations + error handling + CLI)
7. Deploy/demo if ready

**MVP Scope**: ~40 tasks (T001-T037 + T057-T068)

### Incremental Delivery

1. Complete Setup + Foundational (T001-T016) → Foundation ready
2. Add User Story 1 + User Story 4 + CLI (T017-T037, T057-T068) → Test MVP → Deploy/Demo (MVP!)
3. Add User Story 2 (T038-T046) → Test decimals independently → Deploy/Demo
4. Add User Story 3 (T047-T056) → Test negatives independently → Deploy/Demo
5. Polish (T069-T080) → Final quality gates → Deploy/Demo (v1.0)

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T016)
2. Once Foundational is done:
   - **Developer A**: User Story 1 (T017-T025)
   - **Developer B**: User Story 4 (T026-T037)
   - **Developer C**: User Story 2 (T038-T046)
   - **Developer D**: User Story 3 (T047-T056)
3. Developer A or B: CLI Integration (T057-T068) after US1+US4 complete
4. All developers: Polish tasks (T069-T080) in parallel

---

## Task Summary

**Total Tasks**: 80 tasks

**Task Breakdown by Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 8 tasks
- Phase 3 (US1 - Basic Operations): 9 tasks
- Phase 4 (US4 - Error Handling): 12 tasks
- Phase 5 (US2 - Decimals): 9 tasks
- Phase 6 (US3 - Negatives): 10 tasks
- Phase 7 (CLI Integration): 12 tasks
- Phase 8 (Polish): 12 tasks

**Parallel Opportunities**: 45+ tasks can run in parallel (marked with [P])

**MVP Tasks**: 40 tasks (Setup + Foundational + US1 + US4 + CLI Integration)

**Independent Test Criteria**:
- **US1**: Launch calculator, run all 4 operations with integers, verify correct results
- **US4**: Enter invalid inputs (division by zero, alphabets, invalid operators, incomplete), verify error messages and no crashes
- **US2**: Run calculations with decimals, verify precision and formatting
- **US3**: Run calculations with negative numbers, verify correct signed arithmetic
- **CLI**: Run calculator interactively, perform multiple calculations, verify exit works

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability
- **Each user story should be independently completable and testable**
- **TDD requirement**: Verify tests FAIL before implementing (constitution requirement)
- **Type checking**: Run mypy strict mode after each implementation phase
- **Quality gates**: All must pass before completion (pytest, mypy, ruff, coverage ≥95%)
- Commit after each completed user story or logical group
- Stop at any checkpoint to validate story independently
- **Constitution compliance**: All functions <20 lines, type hints on all signatures, edge cases handled
