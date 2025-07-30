from typing import Dict, List
from models.models import Project

class InMemoryProjectRepository:
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self._counter = 1

    def add_project(self, project: Project) -> Project:
        project.id = self._counter
        self.projects[self._counter] = project
        self._counter += 1
        return project

    def get_project(self, project_id: int) -> Project:
        return self.projects.get(project_id)

    def get_all_projects(self) -> List[Project]:
        return list(self.projects.values())
