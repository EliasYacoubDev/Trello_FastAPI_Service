from fastapi import APIRouter, Depends
from schemas.project_schema import ProjectCreation
from database import get_db
from sqlalchemy.orm import Session
from services.users_service import PermissionChecker, get_all_users
from models import project_model

router = APIRouter(tags=["Project Management"])

@router.post("/project", response_model=dict)
async def create_new_project(request: ProjectCreation, db: Session = Depends(get_db), user_data=Depends(PermissionChecker(["admin"]))):
    users = set([id[0] for id in get_all_users(db)])
    requested_users = set(request.users)
    available_users = users.intersection(requested_users)
    for user in available_users:
        project = project_model.Project(
            project_name=request.projectName,
            user_id=user
            )
        db.add(project)
        db.commit()
        db.refresh(project)
    if available_users:
        return {"message": f"Project has been successfully created for the following users:{available_users}"}
    else:
        return {"message": f"Requested users were not found"}
