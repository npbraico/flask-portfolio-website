"""
Unit tests for DAL (Data Access Layer) functions.
"""
import pytest
import DAL


class TestDatabaseInitialization:
    """Test database setup and initialization."""
    
    def test_ensure_db_creates_table(self, test_app):
        """Test that ensure_db creates the projects table."""
        # Table should be created by the fixture
        conn = DAL.sqlite3.connect(DAL.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='projects'"
        )
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None
        assert result[0] == 'projects'
    
    def test_table_has_correct_columns(self, test_app):
        """Test that the projects table has the required columns."""
        conn = DAL.sqlite3.connect(DAL.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(projects)")
        columns = cursor.fetchall()
        conn.close()
        
        column_names = [col[1] for col in columns]
        assert 'id' in column_names
        assert 'title' in column_names
        assert 'description' in column_names
        assert 'ImageFileName' in column_names


class TestAddProject:
    """Test the addProject function."""
    
    def test_add_project_success(self, test_app):
        """Test adding a project successfully."""
        result = DAL.addProject(
            'New Project',
            'A new test project',
            'newproject.png'
        )
        
        assert result is True
    
    def test_add_project_creates_record(self, test_app):
        """Test that adding a project creates a database record."""
        DAL.addProject('Test Project', 'Description', 'image.png')
        
        projects = DAL.getAllProjects()
        assert len(projects) == 1
        assert projects[0]['Title'] == 'Test Project'
        assert projects[0]['Description'] == 'Description'
        assert projects[0]['ImageFileName'] == 'image.png'
    
    def test_add_multiple_projects(self, test_app, sample_projects):
        """Test adding multiple projects."""
        for project in sample_projects:
            DAL.addProject(
                project['title'],
                project['description'],
                project['ImageFileName']
            )
        
        projects = DAL.getAllProjects()
        assert len(projects) == len(sample_projects)


class TestGetAllProjects:
    """Test the getAllProjects function."""
    
    def test_get_all_projects_empty(self, test_app):
        """Test getting projects when database is empty."""
        projects = DAL.getAllProjects()
        assert projects == []
    
    def test_get_all_projects_with_data(self, test_app, populated_db):
        """Test getting all projects when database has data."""
        projects = DAL.getAllProjects()
        
        assert len(projects) == 2
        assert all('id' in p for p in projects)
        assert all('Title' in p for p in projects)
        assert all('Description' in p for p in projects)
        assert all('ImageFileName' in p for p in projects)
    
    def test_get_all_projects_returns_correct_data(self, test_app, populated_db):
        """Test that getAllProjects returns the correct project data."""
        projects = DAL.getAllProjects()
        
        titles = [p['Title'] for p in projects]
        assert 'Test Project 1' in titles
        assert 'Test Project 2' in titles


class TestDeleteProject:
    """Test the deleteProject function."""
    
    def test_delete_project_success(self, test_app, populated_db):
        """Test deleting a project successfully."""
        projects = DAL.getAllProjects()
        project_id = projects[0]['id']
        
        result = DAL.deleteProject(project_id)
        assert result is True
    
    def test_delete_project_removes_record(self, test_app, populated_db):
        """Test that deleting a project removes it from the database."""
        projects_before = DAL.getAllProjects()
        initial_count = len(projects_before)
        
        project_id = projects_before[0]['id']
        DAL.deleteProject(project_id)
        
        projects_after = DAL.getAllProjects()
        assert len(projects_after) == initial_count - 1
    
    def test_delete_nonexistent_project(self, test_app):
        """Test deleting a project that doesn't exist."""
        # Should not raise an error
        result = DAL.deleteProject(99999)
        assert result is True
    
    def test_delete_all_projects(self, test_app, populated_db):
        """Test deleting all projects one by one."""
        projects = DAL.getAllProjects()
        
        for project in projects:
            DAL.deleteProject(project['id'])
        
        remaining_projects = DAL.getAllProjects()
        assert len(remaining_projects) == 0
