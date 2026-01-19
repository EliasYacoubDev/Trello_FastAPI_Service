from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'schema': 'tasks'}
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    task_name = Column(String, nullable=False)
    task_description = Column(String, nullable=True)
    status= Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.projects.id'))
    user_id = Column(Integer, ForeignKey('users.users.id'))
