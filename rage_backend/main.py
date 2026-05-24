import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, DocumentChunk
from schemas import DocumentCreate
from utils import chunk_text,clean_text
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from schemas import SearchQuery
from schemas import AskRequest
import fitz #used to read fPDF content,PyMuPDF lib.
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() #reads .env file
genai.configure( #Authenticates SDK with Gemini API.
    api_key=os.getenv("GEMINI_API_KEY") #retrieves API key 
)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
Base.metadata.create_all(bind=engine)#create all tables using base subclass

@app.post("/documents")
def create_document(document:DocumentCreate):
    db: Session=SessionLocal() #open a new session with the db
    chunks=chunk_text(document.content)
    for ind, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        new_chunk=DocumentChunk(
            document_name=document.title,
            chunk_index=ind,
            content=chunk,
            embedding=embedding
        )
        db.add(new_chunk)
    db.commit()
    db.close()
    return{
        "message":"Chunks created and stored",
        "total_chunks":len(chunks)
    }

@app.post("/search")
def search_documents(search:SearchQuery):
    db:Session=SessionLocal()
    query_embedding=embedding_model.encode(search.query).tolist()
    sql=text("""SELECT content, document_name, chunk_index
        FROM document_chunks
        ORDER BY embedding <->CAST(:query_embedding AS vector)
        LIMIT 2
    """)
    results=db.execute(
        sql,
        {"query_embedding": query_embedding}
    )

    retrieved_chunks = []

    for row in results:
        retrieved_chunks.append({
            "document_name": row.document_name,
            "chunk_index": row.chunk_index,
            "content": row.content
        })

    db.close()

    return {
        "query": search.query,
        "results": retrieved_chunks
    }

@app.post("/ask")
def ask_question(request:AskRequest): #converts JSON into python object for easier processing 
    db:Session=SessionLocal() #open a session
    query_embedding=embedding_model.encode(request.question).tolist()#convert the question into embedding(vector)
    sql = text("""
    SELECT
        content,
        document_name,
        page_number,
        chunk_index
    FROM document_chunks
    ORDER BY embedding <-> CAST(:query_embedding AS vector)
    LIMIT 3
    """) #query for retrieving  and selecting the first n number of content, in terms of semantic distance 
        #compares the stored embedding with the query embedding
    results=db.execute(
        sql,
        {"query_embedding":query_embedding} #sending query embedding and sql to POSTGRESQL
    )
    context_chunks = []
    retrieved_chunks = [] #stores retrieved content
    for row in results:
        context_chunks.append(row.content)
        retrieved_chunks.append({
            "document_name": row.document_name,
            "page_number": row.page_number,
            "chunk_index": row.chunk_index,
            "content": row.content
        })

    context = "\n\n".join(context_chunks) #append retrieved content together
    prompt=f"""
    Answer the asked question ONLY as per the context provided
    Context:{context}
    Question:{request.question}
    """ #VECTORS ARE ONLY FOR COMPARISON, AFTER COMPARING AND SORTING, WE RETRIEVE THE PLAIN TEXT AND THEN FEED IT TO GEMINI
    try:
        response = gemini_model.generate_content(prompt)
        answer = response.text

    except Exception as e:
        answer = "Gemini API temporarily unavailable or quota exceeded."
    db.close()
    return{
        "question":request.question,
        "answer":answer,
        "retrieved_context": retrieved_chunks
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    pdf_bytes = await file.read()

    pdf_document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    db: Session = SessionLocal()

    total_chunks = 0

    for page_number, page in enumerate(pdf_document):

        page_text = page.get_text()
        page_text = clean_text(page_text)

        page_text = " ".join(
        page_text.split()
        )
        chunks = chunk_text(page_text)

        for index, chunk in enumerate(chunks):

            embedding = embedding_model.encode(
                chunk
            ).tolist()

            new_chunk = DocumentChunk(
                document_name=file.filename,
                page_number=page_number + 1,
                chunk_index=index,
                content=chunk,
                embedding=embedding
            )

            db.add(new_chunk)

            total_chunks += 1

    db.commit()

    db.close()

    return {
        "filename": file.filename,
        "total_chunks": total_chunks,
        "message": "PDF processed successfully"
    }

@app.get("/documents")
def get_documents():
    db: Session=SessionLocal()
    documents=db.query(DocumentChunk).all() #==SELECT * FROM documents
    db.close()
    return documents