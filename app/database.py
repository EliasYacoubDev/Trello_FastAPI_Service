from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load the environment variable from the .env file
load_dotenv()

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRESQL_USERNAME')}:{os.getenv('POSTGRESQL_PASSWORD')}@localhost:{os.getenv('POSTGRESQL_PORT')}/{os.getenv('POSTGRESQL_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()