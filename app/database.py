from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/trello"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()