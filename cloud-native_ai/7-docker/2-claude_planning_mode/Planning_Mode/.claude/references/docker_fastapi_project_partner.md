1. Project Memory Configuration (CLAUDE.md)
   Create .claude/CLAUDE.md to give Claude persistent project context:
   
   # Project Architecture
- FastAPI application with async SQLModel + Neon PostgreSQL

- Pydantic v2 for validation and settings management

- Pytest with pytest-asyncio for testing
  
  # Directory Structure

- `app/models/` - SQLModel database models

- `app/routers/` - FastAPI route handlers

- `app/core/` - Config, security, dependencies

- `tests/` - Pytest test suite
  
  # Key Commands

- `pytest -v --cov=app` - Run tests with coverage

- `fastapi dev app/main.py` - Development server

- `alembic upgrade head` - Run migrations (use direct Neon connection)
  
  # Conventions

- Use async/await for all database operations

- NullPool with Neon's PgBouncer for connections

- Pydantic BaseSettings for environment config

- Separate Create/Read/Update schemas per model

  ---

2. Modular Rules for Specific Concerns
   Organize guidelines in .claude/rules/:
   .claude/
   ├── CLAUDE.md
   └── rules/
    ├── api-design.md      # Status codes, response patterns
    ├── testing.md         # Pytest fixtures, async patterns
    ├── database.md        # SQLModel, Neon connection patterns
    └── validation.md      # Pydantic validators, Field usage

  ---

3. Custom Skills for Your Stack
   Skill: FastAPI + SQLModel Patterns
   Create .claude/skills/fastapi-sqlmodel/skill.md:

  ---

  name: fastapi-sqlmodel
  description: Use when creating API endpoints with database models
  allowed-tools: Read, Grep, Glob, Edit

  ---

# FastAPI + SQLModel Patterns

## Model Structure (Separation of Concerns)

  ```python
  class UserBase(SQLModel):
      email: str = Field(index=True)

  class UserCreate(UserBase):
      password: str = Field(min_length=8)

  class User(UserBase, table=True):
      id: int | None = Field(default=None, primary_key=True)
      hashed_password: str

  class UserRead(UserBase):
      id: int

  Async Session Pattern

  async def get_session() -> AsyncGenerator[AsyncSession, None]:
      async with AsyncSession(engine) as session:
          yield session

  ---

## 4. Effective Prompt Patterns

### Be Specific (Reduces Token Usage)

  ```bash

# ❌ Vague

> Add user authentication

# ✅ Specific

> Implement JWT login endpoint in FastAPI:
> 
> - Pydantic models for request/response
> - bcrypt password hashing
> - Return access_token with 30min expiry

  Use File References

# Quick context without full file read

> Explain @app/models/user.py and add email validation

  Iterative Small Changes

> Add the UserPreference SQLModel  # Step 1
> Create CRUD operations for preferences  # Step 2
> Add FastAPI routes for preferences  # Step 3
> Write pytest tests for preference endpoints  # Step 4

  ---

5. Testing Workflow with Pytest
   Ask Claude to Generate Tests
   
   > Write pytest tests for @app/routers/users.py with:
   > 
   > - Async fixtures using pytest-asyncio
   > - In-memory SQLite for isolation
   > - Test happy path and error cases
   > - Use TestClient with dependency overrides
   
   Fix Failing Tests
   
   > Run pytest and fix any failures
   
   Coverage Analysis
   
   > Find functions in @app/services/ not covered by tests
   > Add tests for uncovered edge cases

  ---

6. Database & Neon-Specific Patterns
   Connection Setup Guidance
   
   > Create async SQLModel engine for Neon with:
   > 
   > - NullPool (let Neon's PgBouncer handle pooling)
   > - pool_pre_ping=True for stale connection handling
   > - SSL required
   
   Migration Safety
   
   > Generate Alembic migration for new UserPreference model
   > Use direct connection string (not pooled) for migrations

  ---

7. Hooks for Automation
   Configure .claude/settings.json:
   {
   "hooks": {
    "PostToolUse": [
      {
   
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.file_path' | xargs -I {} sh -c 'echo {} | grep -q \"\\.py$\" && ruff format {} && ruff check --fix {}'"
        }]
   
      }
    ]
   }
   }
   Effect: Auto-formats Python files after every edit.

  ---

8. MCP Server Integrations
   
   # PostgreSQL/Neon - Query database directly
   
   claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres \
   --dsn "$DATABASE_URL"
   
   # GitHub - PR reviews, issue management
   
   claude mcp add github
   
   # Sentry - Error monitoring
   
   claude mcp add sentry
   Usage:
   
   > Query the database for users created today
   > Check Sentry for errors in the auth module
   > Create a PR for these changes

  ---

9. Permission Configuration
   .claude/settings.json:
   {
   "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(python -m alembic:*)",
      "Bash(fastapi:*)",
      "Bash(ruff:*)"
    ],
    "deny": [
      "Read(.env)",
      "Read(**/secrets/**)",
      "Bash(rm -rf:*)"
    ]
   }
   }

  ---

10. Workflow Modes
    
    | Mode        | Use Case                    | Command                       |
    | ----------- | --------------------------- | ----------------------------- |
    | Plan Mode   | Explore before implementing | claude --permission-mode plan |
    | Normal      | Standard development        | Default                       |
    | Auto-Accept | Trusted repetitive tasks    | Shift+Tab to cycle            |
    
    Plan Mode for Complex Features
    claude --permission-mode plan
    
    > Design the user preferences feature with SQLModel and FastAPI
    
    # Claude explores, creates plan, then you approve

  ---

11. Subagents for Specialized Tasks
    Claude automatically uses specialized subagents:
    
    | Task                         | Subagent      |
    | ---------------------------- | ------------- |
    | "Review my changes"          | Code Reviewer |
    | "Explore how auth works"     | Explore Agent |
    | "Run tests and fix failures" | Test Runner   |
    
    Custom Subagent Example
    .claude/agents/api-reviewer.md:

  ---

  name: api-reviewer
  description: Review FastAPI endpoints for security and best practices
  tools: Read, Grep, Glob

  ---

  Check for:

1. Input validation with Pydantic
2. Proper status codes (201 for POST, 204 for DELETE)
3. SQL injection prevention
4. Authentication on protected routes
5. Error handling patterns

  ---

12. Custom Slash Commands
    .claude/commands/test-coverage.md:
    Run pytest with coverage and identify gaps:

13. Execute `pytest --cov=app --cov-report=term-missing`

14. List functions with <80% coverage

15. Suggest which tests to add
    Usage: /test-coverage

  ---

13. Cost Optimization Strategies
    
    | Strategy                    | Savings                     |
    | --------------------------- | --------------------------- |
    | Use @filepath references    | ~30% fewer tokens           |
    | Plan Mode for exploration   | Avoids wasted edits         |
    | Specific prompts            | Reduces clarification loops |
    | Subagents for verbose tasks | Isolates context            |
    
    > /cost  # Check current session usage

  ---

14. Keyboard Shortcuts
    
    | Shortcut  | Action                   |
    | --------- | ------------------------ |
    | Alt+T     | Toggle extended thinking |
    | Shift+Tab | Cycle permission modes   |
    | Ctrl+R    | Search command history   |
    | Escape    | Cancel current operation |

  ---

  Summary: Maximum Efficiency Checklist

| Area        | Action                                                    |
| ----------- | --------------------------------------------------------- |
| Context     | Create .claude/CLAUDE.md with project standards           |
| Rules       | Add .claude/rules/ for domain patterns                    |
| Skills      | Build skills for FastAPI/SQLModel/Pydantic patterns       |
| Prompts     | Be specific, use @file references                         |
| Testing     | Ask Claude to generate + fix tests iteratively            |
| Database    | Use NullPool + Neon PgBouncer, direct conn for migrations |
| Automation  | Set up hooks for formatting/linting                       |
| Integration | Add MCP servers for DB queries, GitHub, monitoring        |
| Workflow    | Use Plan Mode for complex features                        |
| Review      | Leverage code review subagent |
