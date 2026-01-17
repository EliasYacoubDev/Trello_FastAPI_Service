from pydantic import BaseModel
from typing import List

class ProjectCreation(BaseModel):
    projectName: str
    users: List[int]
