# tests/test_main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
from fastapi.testclient import TestClient
from main import app, projects, Project, Dependency

client = TestClient(app)


def test_get_project_dependencies_create_and_fetch():
    # Step 1: Create a project via API
    create_payload = {
        "id": 1,
        "name": "Test Project",
        "description": "A sample test project",
        "dependencies": [
            {"name": "fastapi", "version": "0.100.0", "is_vulnerable": False},
            {"name": "httpx", "version": "0.24.1", "is_vulnerable": True}
        ]
    }

    response = client.post("/projects/", json=create_payload)
    assert response.status_code == 200

    # Step 2: Fetch dependencies for the created project
    dep_response = client.get(f"/projects/{create_payload['id']}/dependencies")
    assert dep_response.status_code == 200
    deps = dep_response.json()

    assert isinstance(deps, list)
    assert any(dep["name"] == "fastapi" for dep in deps)
    assert any(dep["is_vulnerable"] is True for dep in deps if dep["name"] == "httpx")

def test_get_project_dependencies_success():
    # Setup mock project in memory
    project_id = 1
    dependency_list = [
        Dependency(name="fastapi", version="0.100.0", is_vulnerable=False),
        Dependency(name="httpx", version="0.24.1", is_vulnerable=True)
    ]
    projects[project_id] = Project(id=project_id, name="Test Project",description= "A sample test project", dependencies=dependency_list)

    # Fetch dependencies
    response = client.get(f"/projects/{project_id}/dependencies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["name"] == "fastapi"
    assert data[1]["is_vulnerable"] is True


def test_get_project_dependencies_not_found():
    # Ensure project doesn't exist
    project_id = 9999
    projects.pop(project_id, None)

    response = client.get(f"/projects/{project_id}/dependencies")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"
