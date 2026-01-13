"""
Test suite for TasksAPI

This file contains all tests for the FastAPI endpoints defined in main.py.
pytest will automatically discover and run all functions that start with 'test_'.
"""

# Import TestClient from FastAPI - this is a wrapper around httpx
# that allows us to make HTTP requests to our app without running a server
from fastapi.testclient import TestClient

# Import our FastAPI app instance from main.py
from main import app

# Create a TestClient instance
# This client will be used in all our test functions to make requests
# Think of it as a "fake browser" that can call our API endpoints
client = TestClient(app)


# =============================================================================
# TEST 1: Testing the GET /tasks endpoint
# =============================================================================
def test_get_all_tasks():
    """
    Test that GET /tasks returns all tasks.

    This test verifies:
    1. The endpoint returns status code 200 (success)
    2. The response is a list
    3. The list contains 4 tasks
    4. Each task has 'id' and 'task' keys
    """
    # Make a GET request to /tasks
    response = client.get("/tasks")

    # Assert the status code is 200 (OK)
    # If this fails, pytest will show exactly what status code was returned
    assert response.status_code == 200

    # Get the JSON response body
    data = response.json()

    # Assert the response is a list
    assert isinstance(data, list)

    # Assert we have exactly 4 tasks
    assert len(data) == 4

    # Assert the first task has the expected structure
    assert data[0] == {"id": 1, "task": "Buy groceries"}

    # Assert all tasks have required keys
    for task in data:
        assert "id" in task
        assert "task" in task


# =============================================================================
# TEST 2: Testing GET /tasks/{task_id} with path parameter
# =============================================================================
def test_get_single_task():
    """
    Test that GET /tasks/1 returns a single task.

    Path parameters are values embedded in the URL path itself.
    Here, {task_id} is a path parameter.
    """
    # Make a GET request to /tasks/1
    response = client.get("/tasks/1")

    # Assert success
    assert response.status_code == 200

    # Assert the response structure
    data = response.json()
    assert data["id"] == 1
    assert data["task"] == "Buy groceries"
    # When include_details is not provided, it defaults to False
    # so 'details' key should NOT be present
    assert "details" not in data


def test_get_task_with_different_id():
    """
    Test that GET /tasks/5 works with a different task_id.

    This verifies the path parameter is correctly parsed.
    """
    response = client.get("/tasks/5")

    assert response.status_code == 200
    data = response.json()
    # The API returns the task_id we passed
    assert data["id"] == 5


# =============================================================================
# TEST 3: Testing query parameters (include_details)
# =============================================================================
def test_get_task_with_details():
    """
    Test that GET /tasks/1?include_details=true returns task with details.

    Query parameters are key-value pairs after the '?' in a URL.
    Example: /tasks/1?include_details=true

    In FastAPI, bool query params accept: true, false, 1, 0, yes, no
    """
    # Make request with query parameter
    response = client.get("/tasks/1?include_details=true")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["task"] == "Buy groceries"
    # Now 'details' key SHOULD be present
    assert "details" in data
    assert data["details"] == "Go for a walk.."


def test_get_task_without_details_explicit():
    """
    Test that GET /tasks/1?include_details=false explicitly excludes details.
    """
    response = client.get("/tasks/1?include_details=false")

    assert response.status_code == 200

    data = response.json()
    assert "details" not in data


# =============================================================================
# TEST 4: Testing error cases
# =============================================================================
def test_get_task_with_zero_id():
    """
    Test that GET /tasks/0 returns an error.

    According to main.py, task_id < 1 should return an error message.
    """
    response = client.get("/tasks/0")

    assert response.status_code == 200  # Note: API returns 200 with error in body

    data = response.json()
    assert "error" in data
    assert data["error"] == "Task ID must be greater than 0"


def test_get_task_with_negative_id():
    """
    Test that GET /tasks/-1 returns an error.

    Negative IDs should also trigger the validation error.
    """
    response = client.get("/tasks/-1")

    assert response.status_code == 200

    data = response.json()
    assert "error" in data
    assert data["error"] == "Task ID must be greater than 0"


def test_get_task_with_invalid_id_type():
    """
    Test that GET /tasks/abc returns a validation error.

    FastAPI automatically validates that task_id is an integer.
    When we pass a string, it returns a 422 Unprocessable Entity error.
    """
    response = client.get("/tasks/abc")

    # FastAPI returns 422 for validation errors
    assert response.status_code == 422

    # The response will contain validation error details
    data = response.json()
    assert "detail" in data
