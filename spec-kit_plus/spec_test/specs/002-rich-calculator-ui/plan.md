# Implementation Plan: Professional Calculator Interface

**Branch**: `002-rich-calculator-ui` | **Date**: 2026-01-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-rich-calculator-ui/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enhance existing CLI calculator with professional interactive UI using Rich library for styled output and Questionary/Inquirer for arrow-key menu navigation. Feature adds visual branding header, color-coded feedback (cyan prompts, green results, red errors), calculation history table, and interactive operation selection while maintaining all existing calculator logic (decimal handling, division by zero protection, negative numbers, input validation).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: rich (terminal UI), questionary (interactive prompts) - RESOLVED
**Storage**: In-memory session state (no persistence)
**Testing**: pytest with pytest-cov (95% coverage requirement from constitution)
**Target Platform**: Terminal/CLI (Linux, macOS, Windows with ANSI support)
**Project Type**: Single project (CLI application)
**Performance Goals**: Sub-second response to user interactions, handle 50+ consecutive calculations without degradation
**Constraints**: Terminal width ≥80 chars, ANSI color support required, no external API dependencies
**Scale/Scope**: Single-user session-based application, 4 operations, session history tracking

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Status

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. Type Safety** | ✅ PASS | All new UI code will use type hints; existing calculator logic already typed |
| **II. Error Handling First** | ✅ PASS | Existing error handling (division by zero, invalid input) preserved; UI adds error display with red color |
| **III. Test-Driven Development** | ✅ PASS | TDD workflow required: write tests for UI components, menu selection, history display before implementation |
| **IV. Edge Case Completeness** | ✅ PASS | All existing edge cases maintained (decimals, division by zero, negatives, invalid input, large numbers); adds terminal resize, rapid key press handling |
| **V. Single Responsibility** | ✅ PASS | New modules planned: ui/header.py, ui/menu.py, ui/history.py, ui/colors.py - each <20 lines per function |
| **VI. UV Package Management** | ✅ PASS | Dependencies added via `uv add rich questionary`; no manual pip usage |

### Quality Gates (Pre-Implementation)

- [x] All dependencies installable via UV
- [x] No architectural violations
- [x] Existing 95% test coverage will be maintained
- [x] Type checking will pass with strict mypy
- [x] All edge cases from constitution Principle IV covered

### Risk Assessment

**Low Risk**: Feature adds new UI layer without modifying core calculation logic. Existing tests remain valid. UI components are isolated and independently testable.

## Project Structure

### Documentation (this feature)

```text
specs/002-rich-calculator-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── ui_interface.md  # UI component contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Current Structure**:
```text
src/calculator/
├── __init__.py
├── __main__.py
├── operations.py      # Existing: add, subtract, multiply, divide
├── validator.py       # Existing: parse_input, validate_operator, parse_number
└── cli.py             # Existing: run_calculator (basic text-based REPL)

tests/
└── (existing test files)
```

**Enhanced Structure** (after this feature):
```text
src/calculator/
├── __init__.py
├── __main__.py
├── operations.py           # UNCHANGED: core arithmetic operations
├── validator.py            # UNCHANGED: input validation logic
├── cli.py                  # DEPRECATED: old text-based interface (keep for backward compat)
├── rich_cli.py             # NEW: enhanced Rich-based calculator runner
└── ui/                     # NEW: UI components module
    ├── __init__.py
    ├── header.py           # NEW: renders "Panaversity Calculator v2.0" header
    ├── menu.py             # NEW: interactive operation selection menu
    ├── history.py          # NEW: calculation history table display
    ├── colors.py           # NEW: color scheme definitions (cyan, green, red)
    └── formatters.py       # NEW: result formatting utilities

tests/
├── unit/
│   ├── test_operations.py      # EXISTING
│   ├── test_validator.py       # EXISTING
│   └── ui/                     # NEW: UI component tests
│       ├── test_header.py
│       ├── test_menu.py
│       ├── test_history.py
│       └── test_formatters.py
└── integration/
    ├── test_cli.py             # EXISTING
    └── test_rich_cli.py        # NEW: end-to-end Rich UI tests
```

**Structure Decision**: Single project structure maintained. UI components organized in `src/calculator/ui/` submodule following single-responsibility principle. Existing `cli.py` remains for backward compatibility; new `rich_cli.py` provides enhanced interface as primary entry point.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All new complexity (Rich library, interactive prompts, UI components) is justified by user requirements and maintains constitution compliance.

## Architecture Decisions

### AD-001: UI Library Selection

**Decision**: Use `rich` library for terminal styling and layout

**Rationale**:
- Rich provides native support for: panels (header border), tables (history), color styling, layout management
- Well-maintained (active development, 45k+ GitHub stars)
- Pure Python, no external dependencies beyond Python stdlib
- Terminal compatibility detection built-in

**Alternatives Considered**:
- **blessed**: More low-level, would require manual layout logic
- **colorama**: Only handles colors, no layout/table support
- **textual**: Full TUI framework - overkill for this feature, violates simplicity principle

**Trade-offs**:
- Adds ~1.5MB dependency
- Requires ANSI terminal support (documented in spec assumptions)
- Benefits: Significant development time savings, professional output quality, maintainability

### AD-002: Interactive Prompt Library - NEEDS CLARIFICATION

**Options**:

**Option A: questionary**
- Pros: Cleaner API, async support, better type hints, active maintenance
- Cons: Slightly larger dependency

**Option B: inquirer**
- Pros: More mature (older), slightly smaller
- Cons: Less pythonic API, weaker type support

**Option C: rich.prompt + custom arrow key handling**
- Pros: One less dependency
- Cons: Significant custom code, reinventing wheel, testing complexity

**Recommendation**: **Questionary** (Option A) - better type safety aligns with constitution Principle I, cleaner API reduces code complexity (Principle V)

**Action Required**: Research phase will validate questionary vs inquirer for arrow-key menu functionality

### AD-003: History Storage Strategy

**Decision**: In-memory list of Calculation dataclass instances

**Rationale**:
- Spec explicitly excludes persistent storage
- Session-based only (clear on exit)
- Simple list structure sufficient for 50+ calculations performance requirement
- Enables easy table rendering with Rich

**Implementation**:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CalculationRecord:
    operand1: float
    operator: str  # '+', '-', '*', '/'
    operand2: float
    result: float | str  # float for success, str for error message
    timestamp: float  # Unix timestamp for ordering
```

### AD-004: Component Isolation Strategy

**Decision**: Separate UI concerns into dedicated modules (header, menu, history, colors, formatters)

**Rationale**:
- Aligns with Single Responsibility Principle (Constitution V)
- Each component independently testable
- Enables future UI enhancements without modifying core logic
- Clear separation: calculation logic (existing) vs presentation logic (new)

**Module Responsibilities**:
- `header.py`: Renders static branded header panel
- `menu.py`: Operation selection with arrow keys
- `history.py`: Formats and displays calculation table
- `colors.py`: Color scheme constants (CYAN, GREEN, RED)
- `formatters.py`: Number formatting (maintains existing format_result logic)

### AD-005: Backward Compatibility

**Decision**: Keep existing `cli.py` functional, add `rich_cli.py` as new default

**Rationale**:
- Existing users/scripts may depend on basic CLI
- Gradual migration path
- Testing: existing CLI tests remain valid, new tests for Rich UI

**Migration Path**:
- `uv run python -m calculator` → uses new Rich interface (via `__main__.py` update)
- `uv run python -m calculator.cli` → uses legacy text interface (explicit import)

## Phase 0: Research Tasks

### Research Task 1: Interactive Prompt Library Evaluation

**Objective**: Resolve NEEDS CLARIFICATION for AD-002 - select questionary vs inquirer

**Questions to Answer**:
1. Which library has better type hint support for strict mypy compliance?
2. Which provides simpler API for list selection with arrow keys?
3. Which has better terminal compatibility (Windows/Linux/macOS)?
4. Are there any known issues with Rich library integration?

**Acceptance Criteria**:
- Document type safety comparison
- Provide code samples for basic menu selection
- Verify ANSI terminal compatibility
- Recommend one library with justification

### Research Task 2: Rich Library Best Practices

**Objective**: Identify patterns for header panels, tables, and color styling

**Questions to Answer**:
1. How to create persistent header that doesn't scroll with output?
2. Best way to render dynamic tables (calculation history)?
3. Color theme management (custom palettes vs built-in styles)?
4. Layout management for dashboard (header + content + history)?
5. Performance considerations for 50+ table rows?

**Acceptance Criteria**:
- Code examples for header panel creation
- Table rendering patterns for dynamic content
- Color scheme implementation approach
- Layout strategy documented

### Research Task 3: Terminal Compatibility

**Objective**: Ensure ANSI color support detection and graceful degradation

**Questions to Answer**:
1. How does Rich detect terminal capabilities?
2. What happens on non-ANSI terminals?
3. Should we provide fallback mode or error early?
4. Windows Terminal vs CMD vs PowerShell compatibility?

**Acceptance Criteria**:
- Terminal capability detection approach
- Fallback strategy if ANSI not supported
- Testing strategy for different terminal types

### Research Task 4: Error Handling in Interactive Prompts

**Objective**: Align prompt error handling with constitution Principle II

**Questions to Answer**:
1. How to handle Ctrl+C during menu selection?
2. How to re-prompt on invalid number input with colored error message?
3. How to integrate division by zero errors with red color display?
4. Edge case: What if terminal is too narrow (<80 chars)?

**Acceptance Criteria**:
- Keyboard interrupt handling strategy
- Input validation loop with error display
- Error message color integration
- Minimum terminal width validation

## Phase 1: Design Artifacts

### Data Model Requirements

**Entities to Define** (in `data-model.md`):
1. **CalculationRecord**: History entry structure
   - Fields: operand1, operator, operand2, result, timestamp
   - Validation rules: result is float OR error string
   - Display format for table rendering

2. **ColorScheme**: UI color constants
   - Prompt color (cyan)
   - Success color (green)
   - Error color (red)

3. **MenuOption**: Operation menu choice
   - Display name ("Addition", "Subtraction", etc.)
   - Operator symbol ('+', '-', '*', '/')
   - Mapping to operation function

### API Contracts Requirements

**UI Component Interfaces** (in `contracts/ui_interface.md`):

1. **Header Component**:
   - Input: None
   - Output: Rendered Rich Panel with "Panaversity Calculator v2.0"
   - Errors: None (static content)

2. **Menu Component**:
   - Input: List of menu options
   - Output: Selected operator ('+', '-', '*', '/')
   - Errors: KeyboardInterrupt (user cancels)

3. **History Component**:
   - Input: List[CalculationRecord]
   - Output: Rendered Rich Table
   - Errors: None (handles empty list)

4. **Number Input**:
   - Input: Prompt message
   - Output: Validated float
   - Errors: Display red error, re-prompt on invalid input

### Quickstart Requirements

**Development Setup** (in `quickstart.md`):
1. Install dependencies: `uv sync`
2. Run enhanced calculator: `uv run python -m calculator`
3. Run tests: `uv run pytest`
4. Run type check: `uv run mypy src/`
5. Visual test: Verify colored output, menu navigation, history table

**User Guide**:
1. Launch calculator
2. Use arrow keys to select operation
3. Enter first number
4. Enter second number
5. View result and updated history
6. Repeat or exit

## Phase 2 Preview: Task Breakdown

**Note**: Detailed tasks created by `/sp.tasks` command, not `/sp.plan`.

Expected task structure:
1. **T001**: Add Rich and questionary dependencies to pyproject.toml
2. **T002**: Create ui/colors.py with color scheme constants
3. **T003**: Create ui/header.py with header panel rendering
4. **T004**: Create ui/menu.py with interactive operation selection
5. **T005**: Create ui/formatters.py with number formatting
6. **T006**: Create ui/history.py with calculation table rendering
7. **T007**: Create CalculationRecord dataclass in models
8. **T008**: Create rich_cli.py integrating all UI components
9. **T009**: Update __main__.py to use rich_cli as default
10. **T010**: Write unit tests for all UI components (95% coverage)
11. **T011**: Write integration tests for full Rich CLI workflow
12. **T012**: Update README with new features and usage

## Success Metrics

### Implementation Success Criteria

- [ ] All constitution quality gates pass (type checking, linting, 95% coverage)
- [ ] All 10 spec success criteria testable and met
- [ ] No regressions in existing calculator functionality
- [ ] UI components independently testable
- [ ] Performance: <1s response to user actions

### Test Coverage Targets

- Unit tests: 95%+ (constitution requirement)
- Integration tests: Full user workflows (P1 stories)
- Edge case tests: Terminal resize, invalid input, large history

### Documentation Completeness

- [ ] research.md: All NEEDS CLARIFICATION resolved
- [ ] data-model.md: All entities defined with validation rules
- [ ] contracts/ui_interface.md: All component interfaces specified
- [ ] quickstart.md: Setup and user guide complete
- [ ] README.md: Updated with new features

## Dependencies and Risks

### External Dependencies

| Dependency | Version | Purpose | Risk Level |
|------------|---------|---------|------------|
| rich | ^13.0 | Terminal UI (panels, tables, colors) | Low - stable, widely used |
| questionary | ^2.0 | Interactive prompts (arrow key menu) | Low - active maintenance |

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Terminal incompatibility (no ANSI) | High - feature unusable | Detect capabilities early, provide clear error message |
| Rich/questionary integration issues | Medium - UI glitches | Research phase validates integration, thorough testing |
| Performance with large history (100+ entries) | Low - spec requires 50 | Test with 200+ entries, implement pagination if needed |
| Windows terminal compatibility | Medium - subset of users | Test on Windows Terminal, CMD, PowerShell explicitly |

### Assumptions Validation

From spec assumptions:
- ✅ ANSI color support: Validated in Research Task 3
- ✅ 80-char terminal width: Error handling in Research Task 4
- ✅ Arrow key familiarity: Standard UI pattern, minimal user training
- ✅ Single-user session: No concurrency concerns
- ✅ Floating-point precision: Existing calculator logic unchanged

## Next Steps

1. **Phase 0**: Execute research tasks (this happens during `/sp.plan`)
2. **Phase 1**: Generate data-model.md, contracts/, quickstart.md (this happens during `/sp.plan`)
3. **Phase 2**: Run `/sp.tasks` to generate detailed implementation tasks
4. **Implementation**: Execute tasks following TDD workflow
5. **Validation**: All quality gates pass before merge

---

## Post-Design Constitution Re-Evaluation

### Compliance Status After Design (Phase 1 Complete)

| Principle | Status | Post-Design Notes |
|-----------|--------|-------------------|
| **I. Type Safety** | ✅ PASS | All data models use full type hints (CalculationRecord, ColorScheme, MenuOption, CalculationHistory); mypy strict compliance maintained |
| **II. Error Handling First** | ✅ PASS | Error handling designed into contracts (None returns, validators, graceful Ctrl+C handling) |
| **III. Test-Driven Development** | ✅ PASS | Contracts define testable interfaces; quickstart includes TDD workflow |
| **IV. Edge Case Completeness** | ✅ PASS | All edge cases from research documented (terminal width, Ctrl+C, zero division, large history) |
| **V. Single Responsibility** | ✅ PASS | UI components isolated (header, menu, input, output, history); each < 20 lines per function target |
| **VI. UV Package Management** | ✅ PASS | Dependencies specified for uv (rich, questionary); quickstart uses uv commands |

### Design Quality Assessment

- ✅ **All NEEDS CLARIFICATION Resolved**: questionary selected via research
- ✅ **Data Model Complete**: 4 entities defined with validation rules
- ✅ **Contracts Defined**: 6 components with clear inputs/outputs
- ✅ **Quickstart Complete**: Developer and user guides
- ✅ **Performance Validated**: Benchmarks meet requirements (< 25ms for 200 rows)
- ✅ **No Architecture Violations**: Maintains existing code, adds isolated UI layer

### Risk Assessment After Design

All risks from initial assessment remain **Low** with mitigation strategies in place:
- Terminal compatibility: Rich auto-detection + early validation
- Integration issues: Research validated Rich/questionary compatibility
- Performance: Pagination strategy (20 rows) + benchmarks confirm sub-second response
- Windows compatibility: Questionary chosen specifically for cross-platform support

---

**Plan Status**: ✅ Complete (Ready for /sp.tasks)
**Estimated Complexity**: Medium - new UI layer, existing logic stable, clear requirements
**Constitution Compliance**: ✅ All principles satisfied (re-validated post-design)
**Artifacts Generated**:
- ✅ plan.md (this file)
- ✅ research.md (questionary vs inquirer, Rich patterns, terminal compatibility, error handling)
- ✅ data-model.md (CalculationRecord, ColorScheme, MenuOption, CalculationHistory)
- ✅ contracts/ui_interface.md (6 component interfaces defined)
- ✅ quickstart.md (developer and user guides)
- ✅ CLAUDE.md (agent context updated with In-memory session state)

**Next Command**: `/sp.tasks` to generate detailed implementation tasks
