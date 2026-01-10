from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from schemas.user_schema import User, Token
from sqlalchemy.orm import Session
from database import get_db
from models import user_model
from fastapi.security import OAuth2PasswordRequestForm
from services.users_service import authenticate_user, create_access_token, PermissionChecker

router = APIRouter(tags=["User Management"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token = create_access_token(data={"sub": user.name, "role":user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register_user")
async def add_user(request: User, db: Session = Depends(get_db), dependencies=Depends(PermissionChecker(["admin"]))):
    user = user_model.User(
        id=request.id,
        name=request.name,
        email=request.email,
        password=pwd_context.hash(request.password),
        role=request.role
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"User {user.name} created successfully"}
