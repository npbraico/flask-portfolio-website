"""
Integration tests for Flask routes and views.
"""
import pytest
from flask import url_for


class TestBasicRoutes:
    """Test basic page routes."""
    
    def test_about_page(self, client):
        """Test the about page loads successfully."""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'About' in response.data or b'about' in response.data
    
    def test_contact_page(self, client):
        """Test the contact page loads successfully."""
        response = client.get('/contact')
        assert response.status_code == 200
    
    def test_resume_page(self, client):
        """Test the resume page loads successfully."""
        response = client.get('/resume')
        assert response.status_code == 200
    
    def test_root_redirects_to_about(self, client):
        """Test that root URL renders about page."""
        response = client.get('/')
        assert response.status_code == 200


class TestProjectsPage:
    """Test the projects page and functionality."""
    
    def test_projects_page_loads(self, client):
        """Test that the projects page loads successfully."""
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'Projects' in response.data or b'projects' in response.data
    
    def test_projects_page_shows_empty_table(self, client):
        """Test projects page with no projects."""
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'<table' in response.data
    
    def test_projects_page_shows_projects(self, client, populated_db):
        """Test that projects page displays existing projects."""
        response = client.get('/projects')
        
        assert response.status_code == 200
        assert b'Test Project 1' in response.data
        assert b'Test Project 2' in response.data
        assert b'This is a test project description' in response.data
    
    def test_projects_page_shows_images(self, client, populated_db):
        """Test that projects page includes image tags."""
        response = client.get('/projects')
        
        assert b'test1.png' in response.data
        assert b'test2.png' in response.data
        assert b'<img' in response.data
    
    def test_projects_page_has_add_form(self, client):
        """Test that projects page includes the add project form."""
        response = client.get('/projects')
        
        assert b'<form' in response.data
        assert b'title' in response.data
        assert b'description' in response.data
        assert b'image_filename' in response.data or b'ImageFileName' in response.data
    
    def test_projects_page_has_delete_buttons(self, client, populated_db):
        """Test that projects page includes delete buttons."""
        response = client.get('/projects')
        
        assert b'Delete' in response.data or b'delete' in response.data
        assert b'/delete_project/' in response.data


class TestAddProjectRoute:
    """Test the add project functionality."""
    
    def test_add_project_post(self, client):
        """Test adding a project via POST request."""
        response = client.post('/add_project', data={
            'title': 'New Test Project',
            'description': 'This is a new project',
            'image_filename': 'newtest.png'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'New Test Project' in response.data
    
    def test_add_project_redirects_to_projects(self, client):
        """Test that adding a project redirects to projects page."""
        response = client.post('/add_project', data={
            'title': 'Another Project',
            'description': 'Test description',
            'image_filename': 'test.png'
        })
        
        assert response.status_code == 302  # Redirect
        assert '/projects' in response.location
    
    def test_add_project_missing_fields(self, client):
        """Test adding a project with missing fields."""
        response = client.post('/add_project', data={
            'title': 'Incomplete Project'
            # Missing description and image_filename
        }, follow_redirects=True)
        
        # Should still process (description is optional in DB)
        assert response.status_code == 200
    
    def test_add_project_appears_immediately(self, client):
        """Test that new project appears immediately on projects page."""
        # Add a project
        client.post('/add_project', data={
            'title': 'Immediate Project',
            'description': 'Should appear right away',
            'image_filename': 'immediate.png'
        })
        
        # Check it appears on the page
        response = client.get('/projects')
        assert b'Immediate Project' in response.data
        assert b'Should appear right away' in response.data


class TestDeleteProjectRoute:
    """Test the delete project functionality."""
    
    def test_delete_project_post(self, client, populated_db):
        """Test deleting a project via POST request."""
        # Get the first project ID
        import DAL
        projects = DAL.getAllProjects()
        project_id = projects[0]['id']
        
        response = client.post(f'/delete_project/{project_id}', follow_redirects=True)
        
        assert response.status_code == 200
        # Project should not appear on the page anymore
        assert projects[0]['Title'].encode() not in response.data
    
    def test_delete_project_redirects(self, client, populated_db):
        """Test that deleting a project redirects to projects page."""
        import DAL
        projects = DAL.getAllProjects()
        project_id = projects[0]['id']
        
        response = client.post(f'/delete_project/{project_id}')
        
        assert response.status_code == 302  # Redirect
        assert '/projects' in response.location
    
    def test_delete_nonexistent_project(self, client):
        """Test deleting a project that doesn't exist."""
        response = client.post('/delete_project/99999', follow_redirects=True)
        
        # Should not crash, just redirect
        assert response.status_code == 200
    
    def test_delete_reduces_project_count(self, client, populated_db):
        """Test that deleting a project reduces the total count."""
        import DAL
        
        initial_count = len(DAL.getAllProjects())
        projects = DAL.getAllProjects()
        
        client.post(f'/delete_project/{projects[0]["id"]}')
        
        final_count = len(DAL.getAllProjects())
        assert final_count == initial_count - 1


class TestEndToEndWorkflow:
    """Test complete user workflows."""
    
    def test_add_and_delete_workflow(self, client):
        """Test adding a project and then deleting it."""
        # Add a project
        client.post('/add_project', data={
            'title': 'Temporary Project',
            'description': 'Will be deleted',
            'image_filename': 'temp.png'
        })
        
        # Verify it exists
        response = client.get('/projects')
        assert b'Temporary Project' in response.data
        
        # Get its ID and delete it
        import DAL
        projects = DAL.getAllProjects()
        temp_project = [p for p in projects if p['Title'] == 'Temporary Project'][0]
        
        client.post(f'/delete_project/{temp_project["id"]}')
        
        # Verify it's gone
        response = client.get('/projects')
        assert b'Temporary Project' not in response.data
    
    def test_add_multiple_projects_workflow(self, client):
        """Test adding multiple projects in sequence."""
        projects_to_add = [
            ('Project A', 'Description A', 'a.png'),
            ('Project B', 'Description B', 'b.png'),
            ('Project C', 'Description C', 'c.png')
        ]
        
        for title, desc, img in projects_to_add:
            client.post('/add_project', data={
                'title': title,
                'description': desc,
                'image_filename': img
            })
        
        # Verify all are visible
        response = client.get('/projects')
        assert b'Project A' in response.data
        assert b'Project B' in response.data
        assert b'Project C' in response.data
