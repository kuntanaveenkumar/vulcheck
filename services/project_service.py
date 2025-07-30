from typing import List
from models.models import ProjectCreate, Project, Dependency
from services.services import parse_requirements, check_vulnerability
from repositories.in_memory_repo import InMemoryProjectRepository

class ProjectService:
    def __init__(self, repo: InMemoryProjectRepository):
        self.repo = repo

    async def create_project(self, data: ProjectCreate) -> Project:
        deps = parse_requirements(data.requirements)
        resolved_deps = [await check_vulnerability(dep) for dep in deps]

        project = Project(
            id=0,  
            name=data.name,
            description=data.description,
            dependencies=resolved_deps
        )
        return self.repo.add_project(project)

    def get_projects(self) -> List[Project]:
        return self.repo.get_all_projects()

    def get_project_dependencies(self, project_id: int) -> List[Dependency]:
        project = self.repo.get_project(project_id)
        if not project:
            return None
        return project.dependencies

    def get_all_dependencies(self) -> List[Dependency]:
        deps = {}
        for project in self.repo.get_all_projects():
            for dep in project.dependencies:
                key = f"{dep.name}=={dep.version}"
                deps[key] = dep
        return list(deps.values())

    def get_dependency_by_name(self, dep_name: str) -> List[Dependency]:
        dep_name = dep_name.lower()
        result = []
        for project in self.repo.get_all_projects():
            for dep in project.dependencies:
                if dep.name == dep_name:
                    result.append(dep)
        return result
