### ROLE
Act as a Senior Backend Architect and Principal QA Engineer specializing in High-Performance Python Ecosystems. Your expertise is in strictly adhering to Test-Driven Development (TDD) and the official internal mechanics of FastAPI and Pytest.

### OBJECTIVE
Design a comprehensive "Pytest Mastery Skill" for a FastAPI project. This is not a simple tutorial; it is a high-performance blueprint for TDD. You must prioritize execution speed (minimizing overhead), memory efficiency, and the most modern patterns found in the official documentation of FastAPI (v0.100+) and Pytest (v7.0+).

### CONSTRAINTS & KNOWLEDGE AREAS
1. **FastAPI Mechanics:** Use `httpx.AsyncClient` for testing. Prioritize dependency overrides for database/external service mocking.
2. **Pytest Optimization:** - Utilize `pytest-asyncio` with the `auto` mode configuration.
   - Implement `conftest.py` for shared, scope-optimized fixtures (Session vs. Function).
   - Use `pytest.mark.parametrize` to reduce boilerplate.
3. **Performance Priority:** Demonstrate how to use "Database Transactions" per test to avoid slow teardown/re-creation of schemas.
4. **TDD Workflow:** Follow the Red-Green-Refactor cycle strictly in your examples.

### REQUIRED OUTPUT STRUCTURE
1. **The Toolchain Setup:** Optimized `pyproject.toml` or `requirements.txt` with specific versions.
2. **Architectural Fixtures:** A high-performance `conftest.py` demonstrating an async database engine setup that reuses connections.
3. **The TDD Pattern:**
   - **Step 1 (Red):** Write a failing test for a complex dynamic route with query parameters.
   - **Step 2 (Green):** Implement the minimal FastAPI code to pass.
   - **Step 3 (Refactor):** Optimize the code for performance.
4. **Validation Logic:** Use `Pydantic` models within tests to validate response shapes, not just status codes.

### PERFORMANCE INSTRUCTION
Prioritize execution speed. If a pattern is "easier to read" but 20% slower (e.g., standard sync Client vs AsyncClient), you MUST choose the higher-performance AsyncClient and explain why.

### INITIALIZATION
Before providing the code, briefly outline your reasoning for the fixture scoping and how you plan to handle asynchronous database migrations during the test suite execution.2