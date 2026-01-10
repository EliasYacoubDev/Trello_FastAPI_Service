from sqlalchemy import Column, String, Integer
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'users'}
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, primary_key=True, nullable=False)
    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, primary_key=True, nullable=False)
    role = Column(String, primary_key=True, nullable=False)