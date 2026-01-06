# Python Calculator Constitution

<!--
Sync Impact Report:
Version: 1.0.0 (initial constitution creation)
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (6 principles defined)
  - Code Quality Standards
  - Development Workflow
  - Governance
Removed Sections: N/A
Templates Status:
  ✅ plan-template.md: Reviewed - constitution check section compatible
  ✅ spec-template.md: Reviewed - requirements and testing sections aligned
  ✅ tasks-template.md: Reviewed - test-first and task structure compatible
Follow-up TODOs: None
-->

## Core Principles

### I. Type Safety (NON-NEGOTIABLE)

All Python code MUST use type hints for function signatures, class attributes, and complex variable assignments. The project MUST pass strict mypy type checking with no type: ignore comments except where third-party library limitations require it with documented justification.

**Rationale**: Type hints catch bugs early, improve code documentation, enable better IDE support, and make refactoring safer. For a calculator handling numeric operations, type safety prevents subtle bugs from mixing incompatible types.

### II. Error Handling First

Every operation MUST explicitly handle error cases before implementing happy path logic. Division by zero, invalid input types, and numeric overflow MUST be caught and return meaningful error messages, not exceptions that crash the program.

**Rationale**: User input is inherently unreliable. Defensive error handling ensures the calculator is robust and provides clear feedback rather than cryptic stack traces.

### III. Test-Driven Development (NON-NEGOTIABLE)

All features MUST follow strict TDD workflow:
1. Write tests for the feature (including edge cases)
2. Verify tests FAIL
3. Implement minimal code to pass tests
4. Refactor while keeping tests green
5. No implementation code without corresponding tests

**Rationale**: TDD ensures comprehensive test coverage, validates requirements before implementation, and prevents regression bugs. For a calculator, tests verify mathematical correctness across all edge cases.

### IV. Edge Case Completeness

Every calculator operation MUST handle these cases explicitly:
- Decimal precision and rounding
- Division by zero
- Negative numbers in all operations
- Invalid user input (alphabets, special characters, empty input)
- Very large numbers (overflow protection)
- Very small numbers (underflow protection)

**Rationale**: Edge cases are where calculator implementations typically fail. Explicit handling of these cases distinguishes a toy calculator from a reliable tool.

### V. Single Responsibility & Simplicity

Each function MUST do exactly one thing. Calculator operations (add, subtract, multiply, divide) MUST be separate functions. Input validation, parsing, and computation MUST be separate concerns. No function should exceed 20 lines.

**Rationale**: Simple, focused functions are easier to test, debug, and reuse. Following YAGNI (You Ain't Gonna Need It) prevents over-engineering while maintaining clarity.

### VI. UV Package Management

Project MUST use `uv` for all dependency management, virtual environment creation, and script execution. No direct `pip` or `virtualenv` usage. Dependencies MUST be locked in `pyproject.toml` and `uv.lock` for reproducible builds.

**Rationale**: UV provides fast, reliable Python package management with proper dependency locking. Consistent tooling eliminates "works on my machine" problems.

## Code Quality Standards

### Testing Requirements

- **Unit tests**: MUST cover every function with at least 95% code coverage
- **Integration tests**: MUST validate end-to-end user workflows
- **Edge case tests**: MUST include all scenarios from Principle IV
- **Test framework**: pytest with pytest-cov for coverage reporting
- **Test naming**: `test_<function>_<scenario>_<expected_outcome>`

### Code Style

- **Formatter**: ruff format (configured in pyproject.toml)
- **Linter**: ruff check with strict rules enabled
- **Line length**: Maximum 100 characters
- **Docstrings**: Required for all public functions using Google style
- **Type checking**: mypy in strict mode (no implicit Any types)

### Documentation

- **README.md**: MUST include installation instructions using uv, usage examples, and feature list
- **Inline comments**: Only when logic is not self-evident
- **Docstrings**: MUST describe parameters, return types, and raised exceptions
- **Changelog**: Maintain CHANGELOG.md following Keep a Changelog format

## Development Workflow

### Git Workflow

- **Branch naming**: `<issue-number>-<feature-name>` (e.g., `001-basic-operations`)
- **Commit messages**: Follow Conventional Commits (feat:, fix:, test:, docs:, refactor:)
- **Pull requests**: MUST include test evidence and pass all CI checks
- **Reviews**: All code changes require review before merge

### Test-First Discipline

1. Create feature branch
2. Write failing tests in `tests/` directory
3. Verify tests fail with `uv run pytest`
4. Implement feature in `src/` directory
5. Verify tests pass
6. Run type checker: `uv run mypy src/`
7. Run linter: `uv run ruff check src/`
8. Commit with tests and implementation together

### Quality Gates (MUST PASS)

- All tests pass: `uv run pytest`
- Type checking passes: `uv run mypy src/ --strict`
- Linting passes: `uv run ruff check src/`
- Code coverage ≥ 95%: `uv run pytest --cov=src --cov-report=term-missing`
- No unhandled edge cases from Principle IV

## Governance

This constitution supersedes all other development practices for the Python Calculator project. Any deviation from these principles MUST be:

1. Documented in an Architecture Decision Record (ADR)
2. Justified with specific technical or business reasoning
3. Approved before implementation
4. Include a migration plan if changing existing code

All pull requests and code reviews MUST verify compliance with:
- Type hints on all functions and classes
- Test-first development (tests committed before or with implementation)
- Edge case handling (division by zero, invalid input, decimals, negatives)
- Single responsibility (functions < 20 lines, one responsibility each)
- UV-based dependency management (no manual pip usage)

Complexity additions (new dependencies, architectural patterns, abstractions) MUST be justified against the Simplicity principle. The default answer is "no" unless clear benefits outweigh the added complexity.

Constitution amendments MUST:
- Increment version using semantic versioning
- Document rationale in this file
- Update dependent templates in `.specify/templates/`
- Notify all contributors of changes

**Version**: 1.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04
