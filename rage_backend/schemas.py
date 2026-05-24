from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    content: str
class SearchQuery(BaseModel):
    query: str
class AskRequest(BaseModel):
    question:str