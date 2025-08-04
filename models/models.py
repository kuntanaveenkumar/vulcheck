from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Annotated


class ProjectCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100, description="Project name")]
    description: Annotated[Optional[str], Field(default=None, max_length=300)]
    requirements: Annotated[str, Field(description="Raw requirements.txt content")]

    @field_validator("requirements")
    @classmethod
    def validate_requirements_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Requirements cannot be empty.")
        return value


class Vulnerability(BaseModel):
    id: Optional[str] = Field(None, description="Unique ID of the vulnerability")
    description: Optional[str] = Field(None, description="Description of the vulnerability")
    severity: Optional[str] = Field(None, description="Severity (e.g. LOW, MEDIUM, HIGH)")
    

class Dependency(BaseModel):
    name: Annotated[str, Field(min_length=1, description="Dependency name")]
    version: Annotated[str, Field(pattern=r"^[0-9]+(\.[0-9]+)*$", description="Version string in semantic versioning")]
    is_vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)

    @field_validator("vulnerabilities")
    @classmethod
    def validate_vulnerabilities_match_flag(cls, value: List[Vulnerability], values) -> List[Vulnerability]:
        is_vulnerable = values.get("is_vulnerable")
        if is_vulnerable and not value:
            raise ValueError("Vulnerable dependencies must include at least one vulnerability detail.")
        return value

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    dependencies: List[Dependency] = Field(default_factory=list)
