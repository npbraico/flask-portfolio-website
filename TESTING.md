# Flask Website Testing Guide

## Overview
This test suite provides comprehensive testing for the Flask website with database-driven projects functionality.

## Test Files

- **conftest.py** - Pytest fixtures and configuration
  - `test_app` - Flask app with temporary test database
  - `client` - Test client for making requests
  - `sample_projects` - Sample project data
  - `populated_db` - Database populated with test projects

- **test_dal.py** - Unit tests for Data Access Layer
  - Database initialization tests
  - `addProject()` tests
  - `getAllProjects()` tests
  - `deleteProject()` tests

- **test_routes.py** - Integration tests for Flask routes
  - Basic page routes (about, contact, resume)
  - Projects page rendering
  - Add project functionality
  - Delete project functionality
  - End-to-end workflows

## Running Tests

### Install test dependencies
```powershell
pip install -r requirements.txt
```

### Run all tests
```powershell
pytest
```

### Run with coverage report
```powershell
pytest --cov=. --cov-report=html
```

### Run specific test file
```powershell
pytest test_dal.py
pytest test_routes.py
```

### Run specific test class
```powershell
pytest test_dal.py::TestAddProject
pytest test_routes.py::TestProjectsPage
```

### Run specific test function
```powershell
pytest test_dal.py::TestAddProject::test_add_project_success
```

### Run with verbose output
```powershell
pytest -v
```

### Run and show print statements
```powershell
pytest -s
```

## Test Coverage

The test suite covers:

✅ Database initialization and schema validation
✅ Adding projects to the database
✅ Retrieving all projects from the database
✅ Deleting projects from the database
✅ All Flask routes (about, contact, resume, projects)
✅ Projects page rendering with and without data
✅ Add project form submission and redirect
✅ Delete project functionality
✅ End-to-end user workflows
✅ Edge cases (empty database, nonexistent projects)

## Continuous Integration

To run tests in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=. --cov-report=xml
```

## Test Database

Tests use a temporary SQLite database that is:
- Created fresh for each test session
- Automatically cleaned up after tests complete
- Isolated from the production `projects.db`

This ensures tests don't affect your real data.

## Writing New Tests

Follow these patterns:

```python
def test_descriptive_name(client, test_app):
    """Clear docstring explaining what is tested."""
    # Arrange - set up test data
    # Act - perform the action
    # Assert - verify the results
    assert expected == actual
```

Use fixtures from `conftest.py`:
- `client` - for route testing
- `test_app` - for app configuration
- `sample_projects` - for test data
- `populated_db` - for tests needing existing data
