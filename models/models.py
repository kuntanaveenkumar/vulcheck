from pydantic import BaseModel
from typing import List, Dict, Optional

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    requirements: str  

class Dependency(BaseModel):
    name: str
    version: str
    is_vulnerable: bool = False
    vulnerabilities: List[dict] = []

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    dependencies: List[Dependency]
