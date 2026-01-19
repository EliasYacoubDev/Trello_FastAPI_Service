from fastapi import APIRouter, Depends, HTTPException
from schemas.task_schema import TaskCreation, TaskUpdate
from database import get_db
from sqlalchemy.orm import Session
from services.users_service import PermissionChecker
from models.task_model import Task

router = APIRouter(tags=["Task Management"])

@router.post("/task", response_model=dict)
async def create_new_task(request: TaskCreation, db: Session = Depends(get_db), user_data=Depends(PermissionChecker(["admin"]))):
    task = Task(
        task_name=request.tasktName,
        task_description=request.taskDescription,
        status=request.status,
        project_id=request.projectID,
        user_id=request.users
        )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task.task_name} has been successfully created for user {task.user_id}"}


@router.put("/task/{task_name}", response_model=dict)
async def update_task(task_name:str, task_update:TaskUpdate, db: Session = Depends(get_db), user_id: str = Depends(PermissionChecker.verify_user_id)):
    task=db.query(Task).filter(Task.task_name == task_name).first()
    if task.user_id != user_id:
        raise HTTPException(status_code=404, detail="User not authorized to change the task")
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    return {"message": f"Task {task.task_name} has been successfully updated"}

