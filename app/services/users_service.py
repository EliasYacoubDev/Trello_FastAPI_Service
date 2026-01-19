from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, ExpiredSignatureError
from models.user_model import User
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import List
from dotenv import load_dotenv
import os

# Load the environment variable from the .env file
load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_user(db: Session, username: str):
    return db.query(User).filter(User.email == username).first()

def get_all_users(db:Session):
    return db.query(User.id).all()

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    enocded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return enocded_jwt
            
class PermissionChecker:
    def __init__(self, required_permissions: List[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(oauth2_scheme)) -> None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_permissions = payload.get("role", [])
            for perm in self.required_permissions:
                if perm not in user_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission '{perm}' is required"
                    )
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        
    def verify_user_id(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = payload.get("id", [])
            return user_id
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
