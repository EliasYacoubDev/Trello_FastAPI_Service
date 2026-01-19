from pydantic import BaseModel
from typing import Optional

class TaskCreation(BaseModel):
    tasktName: str
    taskDescription: str
    status: str
    users: int
    projectID: int

class TaskUpdate(BaseModel):
    taskDescription: Optional[str] = None
    status: Optional[str] = None
