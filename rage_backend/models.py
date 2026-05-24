from sqlalchemy import Column, Integer, String, Text
from database import Base
from pgvector.sqlalchemy import Vector

class DocumentChunk(Base):
    __tablename__="document_chunks"
    id=Column(Integer,primary_key=True,index=True)
    document_name=Column(String)
    chunk_index=Column(Integer)
    page_number = Column(Integer)
    content=Column(Text)
    embedding=Column(Vector(384))
#ORM Mapping-> define tables using Pythonobjects, instead of writing raw sql manually