from fastapi import APIRouter, HTTPException
from typing import List
from models.models import ProjectCreate, Project, Dependency
from services.project_service import ProjectService
from repositories.in_memory_repo import InMemoryProjectRepository

router = APIRouter()
service = ProjectService(InMemoryProjectRepository())

@router.post("/projects", response_model=Project)
async def create_project(data: ProjectCreate):
    return await service.create_project(data)

@router.get("/projects", response_model=List[Project])
def get_projects():
    return service.get_projects()

@router.get("/projects/{project_id}/dependencies", response_model=List[Dependency])
def get_project_dependencies(project_id: int):
    deps = service.get_project_dependencies(project_id)
    if deps is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return deps

@router.get("/dependencies", response_model=List[Dependency])
def get_all_dependencies():
    return service.get_all_dependencies()

@router.get("/dependencies/{dep_name}", response_model=List[Dependency])
def get_dependency(dep_name: str):
    deps = service.get_dependency_by_name(dep_name)
    if not deps:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return deps
