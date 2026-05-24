from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/rag_db"
#postgresql->db type, postgres->username,password, localhost, 5432->port, rag_db->database name
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base=declarative_base()
#Base->all the tables inherit from this