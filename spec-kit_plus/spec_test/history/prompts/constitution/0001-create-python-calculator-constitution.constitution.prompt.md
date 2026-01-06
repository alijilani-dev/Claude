---
id: 0001
title: Create Python Calculator Constitution
stage: constitution
date: 2026-01-04
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: unknown
command: sp.constitution
labels: ["constitution", "setup", "python", "calculator", "uv", "type-hints"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution creation)
---

## Prompt

in this project we will be creating a calculator in python. my project will be setup with uv. we will use type hints.

## Response snapshot

Created Python Calculator Constitution v1.0.0 with 6 core principles:

1. **Type Safety (NON-NEGOTIABLE)**: All code must use type hints and pass strict mypy checking
2. **Error Handling First**: Explicit handling of division by zero, invalid input, decimals, negatives
3. **Test-Driven Development (NON-NEGOTIABLE)**: Strict TDD workflow with failing tests before implementation
4. **Edge Case Completeness**: Mandatory handling of decimal precision, division by zero, negative numbers, invalid input, overflow/underflow
5. **Single Responsibility & Simplicity**: Functions < 20 lines, one responsibility, YAGNI principles
6. **UV Package Management**: All dependency management through uv, no direct pip usage

Additional sections defined:
- **Code Quality Standards**: pytest with 95% coverage, ruff formatting/linting, mypy strict mode, Google-style docstrings
- **Development Workflow**: Git workflow with conventional commits, test-first discipline, quality gates
- **Governance**: Constitution enforcement, amendment procedures, compliance verification

All templates reviewed for compatibility. No follow-up actions required.

## Outcome

- ✅ Impact: Project constitution established with Python-specific principles for calculator development
- 🧪 Tests: N/A (constitution is policy document, not code)
- 📁 Files: Created .specify/memory/constitution.md (v1.0.0)
- 🔁 Next prompts: /sp.specify to create feature specification, or begin implementing calculator features following TDD principles
- 🧠 Reflection: Constitution captures user's uv and type hints requirements while adding essential calculator-specific edge case handling principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution creation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
