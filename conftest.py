"""
Pytest configuration and fixtures for Flask website testing.
"""
import pytest
import os
import tempfile
import sqlite3
from website import app
import DAL


@pytest.fixture
def test_app():
    """Create and configure a test instance of the Flask app."""
    # Use a temporary database for testing
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Override the database path in DAL
    original_db = DAL.DB_NAME
    DAL.DB_NAME = db_path
    
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize the test database
    DAL.ensure_db()
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    DAL.DB_NAME = original_db


@pytest.fixture
def client(test_app):
    """Create a test client for the Flask app."""
    return test_app.test_client()


@pytest.fixture
def runner(test_app):
    """Create a test CLI runner for the Flask app."""
    return test_app.test_cli_runner()


@pytest.fixture
def sample_projects():
    """Sample project data for testing."""
    return [
        {
            'title': 'Test Project 1',
            'description': 'This is a test project description',
            'ImageFileName': 'test1.png'
        },
        {
            'title': 'Test Project 2',
            'description': 'Another test project',
            'ImageFileName': 'test2.png'
        }
    ]


@pytest.fixture
def populated_db(test_app, sample_projects):
    """Populate the test database with sample projects."""
    for project in sample_projects:
        DAL.addProject(
            project['title'],
            project['description'],
            project['ImageFileName']
        )
    return sample_projects
