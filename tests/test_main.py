import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from models.models import Dependency, Vulnerability
# Fix import path


from main import app

client = TestClient(app)

mock_requirements = "fastapi==0.100.0\nhttpx==0.24.1"

@pytest.fixture
def create_project_payload():
    return {
        "name": "Test Project",
        "description": "A test project",
        "requirements": mock_requirements
    }

@patch("services.services.parse_requirements")
@patch("services.services.check_vulnerability", new_callable=AsyncMock)
def test_create_project(mock_check_vuln, mock_parse, create_project_payload):
    mock_parse.return_value = [
        {"name": "fastapi", "version": "0.100.0"},
        {"name": "httpx", "version": "0.24.1"}
    ]

    def fake_check_vuln(dep_dict):
        return Dependency(
            name="httpx",
            version="0.24.1",
            is_vulnerable=True,
            vulnerabilities=[
                {
                "id": "PYSEC-2024-38",
                "severity": "low",
                "description": "test vuln"
                }
            ]
        )

    mock_check_vuln.side_effect = fake_check_vuln

    response = client.post("/projects", json=create_project_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert len(data["dependencies"]) == 2
    assert any(d["is_vulnerable"] for d in data["dependencies"])
    
def test_get_all_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)

def test_get_project_dependencies_success():
    # Assume project ID 1 was created in previous test
    response = client.get("/projects/1/dependencies")
    assert response.status_code == 200
    deps = response.json()
    assert any(d["name"] == "httpx" for d in deps)

def test_get_project_dependencies_not_found():
    response = client.get("/projects/9999/dependencies")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

def test_get_all_dependencies():
    response = client.get("/dependencies")
    assert response.status_code == 200
    deps = response.json()
    assert isinstance(deps, list)

def test_get_dependency_by_name_success():
    response = client.get("/dependencies/httpx")
    assert response.status_code == 200
    deps = response.json()
    assert all(dep["name"].lower() == "httpx" for dep in deps)

def test_get_dependency_by_name_not_found():
    response = client.get("/dependencies/nonexistentlib")
    assert response.status_code == 404
    assert response.json()["detail"] == "Dependency not found"
