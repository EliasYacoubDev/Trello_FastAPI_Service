from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base

class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {'schema': 'projects'}
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    project_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.users.id'))