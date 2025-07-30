from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models.models import ProjectCreate, Project, Dependency
from services.services import parse_requirements, check_vulnerability

app = FastAPI()
projects: Dict[int, Project] = {}
project_id_counter = 1

@app.post("/projects", response_model=Project)
async def create_project(data: ProjectCreate):
    global project_id_counter

    deps = parse_requirements(data.requirements)
    resolved_deps = [await check_vulnerability(dep) for dep in deps]

    project = Project(
        id=project_id_counter,
        name=data.name,
        description=data.description,
        dependencies=resolved_deps
    )

    projects[project_id_counter] = project
    project_id_counter += 1
    return project

@app.get("/projects", response_model=List[Project])
def get_projects():
    return list(projects.values())

@app.get("/projects/{project_id}/dependencies", response_model=List[Dependency])
def get_project_dependencies(project_id: int):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id].dependencies

@app.get("/dependencies", response_model=List[Dependency])
def get_all_dependencies():
    dep_map: Dict[str, Dependency] = {}

    for project in projects.values():
        for dep in project.dependencies:
            key = f"{dep.name}=={dep.version}"
            dep_map[key] = dep

    return list(dep_map.values())

@app.get("/dependencies/{dep_name}", response_model=List[Dependency])
def get_dependency(dep_name: str):
    dep_name = dep_name.lower()
    deps = []
    for project in projects.values():
        for dep in project.dependencies:
            if dep.name == dep_name:
                deps.append(dep)
    if not deps:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return deps
